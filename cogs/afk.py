
import discord
from discord.ext import commands
from datetime import datetime, timezone

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def afk(self, ctx, *, reason="AFK"):
        await self.bot.db.execute("INSERT OR REPLACE INTO afk VALUES(?,?,?,?,?)",
        (ctx.author.id, reason, datetime.now(timezone.utc).isoformat(),0,""))
        embed = discord.Embed(title="AFK Set", description=f"{ctx.author.mention} is now AFK: {reason}", color=0x3498db, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)

    def _is_afk_command_message(self, message):
        if not message.content:
            return False
        check = message.content.strip().lower()
        return check.startswith("?afk")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self._is_afk_command_message(message):
            return

        row = await self.bot.db.fetchone("SELECT * FROM afk WHERE user_id=?", (message.author.id,))
        if row:
            await self.bot.db.execute("DELETE FROM afk WHERE user_id=?", (message.author.id,))
            embed = discord.Embed(title="Welcome Back", description=f"Welcome back {message.author.mention}", color=0x00ff00, timestamp=discord.utils.utcnow())
            await message.channel.send(embed=embed)

        for m in message.mentions:
            row = await self.bot.db.fetchone("SELECT reason,started FROM afk WHERE user_id=?", (m.id,))
            if row:
                embed = discord.Embed(title="AFK Reminder", description=f"{m.display_name} is AFK: {row[0]}", color=0xffcc00, timestamp=discord.utils.utcnow())
                await message.channel.send(embed=embed)

async def setup(bot): await bot.add_cog(AFK(bot))
