import discord
from discord.ext import commands
import logging

class Logging(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        logging.exception(error)
        embed = discord.Embed(title="Command Error", description=str(error), color=0xff0000, timestamp=discord.utils.utcnow())
        await ctx.send(embed=embed)

async def setup(bot): await bot.add_cog(Logging(bot))
