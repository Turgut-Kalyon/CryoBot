
import sys
from discord.ext import commands
import traceback

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print("Fehler bei Command-Ausführung:")
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await ctx.send(f"⚠️ Ein Fehler ist aufgetreten: `{error}`")
