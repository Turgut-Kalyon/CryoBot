"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
from discord.ext import commands


class Game(commands.Cog):
    def __init__(self):
        super().__init__()
        self.game_name = None

