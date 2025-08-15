"""
Author: Turgut Kalyon
Description: Main entry point for the CryoBot application.
This script initializes the CryoBot, loads environment variables, and sets up cogs.
"""
import os

import discord
from discord.ext import commands

class CryoBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
