"""
Author: Turgut Kalyon
Description: Main entry point for the CryoBot application.
This script initializes the CryoBot, loads environment variables, and sets up cogs.
"""
import discord# pragma: no cover
from discord.ext import commands# pragma: no cover

class CryoBot(commands.Bot):# pragma: no cover

    def __init__(self):# pragma: no cover
        super().__init__(command_prefix='!', intents=discord.Intents.all())# pragma: no cover
    async def on_ready(self):# pragma: no cover
        print(f'Logged in as {self.user} (ID: {self.user.id})')
