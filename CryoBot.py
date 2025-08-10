"""
Author: Turgut Kalyon
Description: Main entry point for the CryoBot application.
This script initializes the CryoBot, loads environment variables, and sets up cogs.
"""

import discord
from discord.ext import commands

class CryoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        if self.is_message_from_bot(message):
            return
        if self.is_message_hello_cmd(message):
            await message.channel.send(f'Hallo {message.author.mention}')
        await self.process_commands(message)

    @staticmethod
    def is_message_hello_cmd(message):
        return message.content == '!hallo'

    def is_message_from_bot(self, message):
        return message.author == self.user

    
