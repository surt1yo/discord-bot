
import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot): self.bot=bot

    @commands.hybrid_command()
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(title="Pong", description=f"{self.bot.latency*1000:.0f}ms", color=0x00ff00, timestamp=discord.utils.utcnow()))

    @commands.hybrid_command()
    async def help(self, ctx):
        await ctx.send(embed=discord.Embed(title="Commands", description="?ping ?afk ?purge ?uptime ?botstats", color=0x3498db, timestamp=discord.utils.utcnow()))

async def setup(bot): await bot.add_cog(General(bot))
