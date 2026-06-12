
import asyncio
import json
import logging
import os
import sys
import time
import discord
from discord.ext import commands
from config import TOKEN, LOG_LEVEL
from database import Database

COGS = ["general", "afk", "admin", "stats", "bot-logging", "webcam"]
RESTART_NOTIFICATION = "restart_notify.json"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    filename="logs/bot.log",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        # Support both the ? prefix and bot mention as prefixes
        super().__init__(command_prefix=commands.when_mentioned_or("?"), intents=intents, help_command=None)
        self.db = Database("data/bot.db")
        self.started = time.time()
        self._cog_mtimes = {}
        self._watch_task = None
        self._restart_complete_sent = False

    async def setup_hook(self):
        await self.db.connect()
        await self.db.init()
        for cog in COGS:
            await self.load_extension(f"cogs.{cog}")
        await self.tree.sync()
        logging.info("Slash commands synced")
        self._watch_task = self.loop.create_task(self._auto_reload_cogs())

    async def _auto_reload_cogs(self, interval: float = 2.0):
        await self.wait_until_ready()
        self._cog_mtimes = {cog: self._get_cog_mtime(cog) for cog in COGS}
        while not self.is_closed():
            await asyncio.sleep(interval)
            for cog in COGS:
                mtime = self._get_cog_mtime(cog)
                if mtime is None:
                    continue
                previous = self._cog_mtimes.get(cog)
                if previous is None:
                    self._cog_mtimes[cog] = mtime
                    continue
                if mtime != previous:
                    try:
                        await self.reload_extension(f"cogs.{cog}")
                        logging.info("Reloaded cog cogs.%s because its file changed", cog)
                    except Exception as exc:
                        logging.exception("Failed to auto-reload cog cogs.%s", cog)
                    self._cog_mtimes[cog] = mtime

    @staticmethod
    def _get_cog_mtime(cog: str):
        path = os.path.join("cogs", f"{cog}.py")
        if not os.path.exists(path):
            return None
        return os.path.getmtime(path)

    async def on_ready(self):
        logging.info(f"Started as {self.user}")
        await self._maybe_send_restart_complete()

    async def on_command(self, ctx):
        logging.info("Command: %s by %s", ctx.command, ctx.author)

    async def _maybe_send_restart_complete(self):
        if self._restart_complete_sent:
            return
        if not os.path.exists(RESTART_NOTIFICATION):
            return

        try:
            with open(RESTART_NOTIFICATION, "r", encoding="utf-8") as f:
                data = json.load(f)
            channel_id = data.get("channel_id")
        except Exception:
            channel_id = None

        try:
            os.remove(RESTART_NOTIFICATION)
        except OSError:
            pass

        if not channel_id:
            self._restart_complete_sent = True
            return

        channel = self.get_channel(channel_id)
        if channel is None:
            try:
                channel = await self.fetch_channel(channel_id)
            except Exception:
                channel = None

        if channel is None:
            self._restart_complete_sent = True
            return

        embed = discord.Embed(
            title="Restart Complete",
            description="The bot has restarted successfully.",
            color=0x00ff00,
            timestamp=discord.utils.utcnow(),
        )
        try:
            await channel.send(embed=embed)
        except Exception:
            pass
        self._restart_complete_sent = True

bot = Bot()

if __name__ == "__main__":
    bot.run(TOKEN)
