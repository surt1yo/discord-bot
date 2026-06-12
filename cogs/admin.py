
import json
import os
import sys

import discord
from discord.ext import commands

COGS = ["general", "afk", "admin", "stats", "logging"]
RESTART_NOTIFICATION = "restart_notify.json"

class Admin(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @commands.hybrid_command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx,amount:int):
        await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(title="Purge", description=f"Deleted {amount} messages.", color=0xff0000, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed, delete_after=5)

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self,ctx,user:discord.User):
        await self.bot.db.execute("INSERT OR IGNORE INTO blacklist VALUES(?)",(user.id,))
        embed = discord.Embed(title="Blacklist", description=f"{user.mention} has been blacklisted.", color=0xffa500, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def whitelist(self,ctx,user:discord.User):
        await self.bot.db.execute("INSERT OR IGNORE INTO whitelist VALUES(?)",(user.id,))
        embed = discord.Embed(title="Whitelist", description=f"{user.mention} has been whitelisted.", color=0x00ff00, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="reload")
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str = None):
        if cog:
            target = f"cogs.{cog}"
            await self.bot.reload_extension(target)
            description = f"Reloaded `{target}`."
        else:
            for extension in COGS:
                await self.bot.reload_extension(f"cogs.{extension}")
            description = "Reloaded all cogs."
        embed = discord.Embed(title="Reload Complete", description=description, color=0x00ff00, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="restart")
    @commands.is_owner()
    async def restart_bot(self, ctx):
        notification_data = {"channel_id": ctx.channel.id}
        try:
            with open(RESTART_NOTIFICATION, "w", encoding="utf-8") as f:
                json.dump(notification_data, f)
        except Exception:
            pass

        embed = discord.Embed(title="Restarting", description="Bot is restarting now.", color=0xffcc00, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)
        await self.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)

async def setup(bot): await bot.add_cog(Admin(bot))
