import discord
from discord.ext import commands


class Webcam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="webcam")
    async def webcam(self, ctx: commands.Context, *, target: str = None):
        # Expect command usage like: ?webcam-moniter(USERNAME: USER ID)/broadcast-Moniter-2
        # We'll parse the raw message after the invoked command
        raw = ctx.message.content[len(str(ctx.prefix or "")) + len(str(ctx.invoked_with or "")):].strip()
        if not raw:
            return await ctx.send("Invalid format. Use: ?webcam-moniter(USERNAME: USER ID)/broadcast-Moniter-2")

        parts = [p.strip() for p in raw.split("/") if p.strip()]
        if len(parts) != 2:
            return await ctx.send("Invalid format. Use: ?webcam-moniter(USERNAME: USER ID)/broadcast-Moniter-2")

        user_part, broadcast_part = parts

        # parse user part like: moniter(USERNAME: USER ID)
        if "(" not in user_part or ")" not in user_part:
            return await ctx.send("Invalid user segment. Expected: moniter(USERNAME: USER ID)")

        name_segment = user_part.split("(", 1)[0].strip()
        user_inside = user_part.split("(", 1)[1].rsplit(")", 1)[0].strip()

        # parse username and id inside parentheses: USERNAME: USER ID
        if ":" not in user_inside:
            return await ctx.send("Invalid user segment. Expected: (USERNAME: USER ID)")

        username, userid = [s.strip() for s in user_inside.split(":", 1)]

        # parse broadcast part like: broadcast-Moniter-2
        if "-" not in broadcast_part:
            return await ctx.send("Invalid broadcast segment. Expected: broadcast-Moniter-2")

        action, monitor = [s.strip() for s in broadcast_part.split("-", 1)]

        # basic validation
        if name_segment.lower() != "moniter" or action.lower() != "broadcast":
            return await ctx.send("Invalid format. Use: ?webcam-moniter(USERNAME: USER ID)/broadcast-Moniter-2")

        await ctx.send(f"Broadcasting webcam for {username} (ID: {userid}) on {monitor}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Webcam(bot))
