"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
import asyncio
from abc import abstractmethod
from discord.ext import commands
from cogs.Games.BetFactory import BetFactory
from cogs.Games.BetValidator import BetValidator
from cogs.Games.GameValidator import GameValidator

class Game(commands.Cog):

    def __init__(self, bot, coin_storage, minimum_bet = None, maximum_bet = None):
        super().__init__()
        self.bot = bot
        self.bet_validator = BetValidator(minimum_bet, maximum_bet)
        self.game_validator = GameValidator()
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
        self.coin_storage = coin_storage
        self.current_bet = None

    async def asking_for_bet(self, ctx):
        if not await self.can_player_start_game(ctx):
            return None
        await self.send_bet_request_message(ctx)
        return await self.get_valid_bet(ctx)


    async def get_valid_bet(self, ctx):
        while True:
            bet = await self.wait_for_bet_message(ctx)
            if await self.bet_validator.is_bet_permitted(bet):
                self.current_bet = BetFactory.create_bet(int(bet.content), ctx.author.id)
                return self.current_bet
            if await self.is_quitting(bet):
                return None

    async def wait_for_bet_message(self, ctx):
        try:
            return await self.bot.wait_for(
                'message',
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
        except asyncio.TimeoutError:
            await ctx.send("Zeitüberschreitung: Du hast zu lange gebraucht, um deinen Einsatz zu nennen.")
            return None

    @abstractmethod
    async def start_game(self):
        raise NotImplementedError("This method should be overridden by subclasses.")