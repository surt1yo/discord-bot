
import discord, platform
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @commands.command()
    async def uptime(self,ctx):
        embed = discord.Embed(title="Uptime", description="Running", color=0x00ff00, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)

    @commands.command()
    async def botstats(self,ctx):
        e=discord.Embed(title="Bot Stats",color=0x7289da, timestamp=discord.utils.utcnow())
        e.add_field(name="Guilds",value=len(self.bot.guilds))
        e.add_field(name="Users",value=len(self.bot.users))
        e.add_field(name="Python",value=platform.python_version())
        e.add_field(name="Discord.py",value=discord.__version__)
        await ctx.send(embed=e)

async def setup(bot): await bot.add_cog(Stats(bot))
