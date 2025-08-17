"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
from discord.ext import commands


class Game(commands.Cog):

    def __init__(self):
        super().__init__()


class Roulette(Game):
    """
    A class representing a Roulette game.
    This class can be extended to implement specific game logic.
    """
    def __init__(self):
        super().__init__()

