"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
import asyncio
from abc import abstractmethod
from discord.ext import commands
from Messenger.Game_Messenger import GameMessenger
from account import AccountRepository, AccountService
from cogs.Games.BetFactory import BetFactory
from cogs.Games.BetValidator import BetValidator
from cogs.Games.GameValidator import GameValidator

class Game(commands.Cog):

    def __init__(self, bot, repo: AccountRepository, minimum_bet=None, maximum_bet=None):
        super().__init__()
        self.bot = bot
        self.bet_validator = BetValidator(minimum_bet, maximum_bet)
        self.game_validator = GameValidator()
        self.account_service = AccountService(repo)
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
        self.current_bet = None
        self.game_messenger = GameMessenger(bot.channel, self.minimum_bet, self.maximum_bet, self.bet_validator)

    async def asking_for_bet(self, ctx):
        if not await self.can_player_start_game(ctx):
            return None
        await self.game_messenger.send_bet_request_message(ctx, self.maximum_bet, self.minimum_bet)
        return await self.get_valid_bet(ctx)


    async def get_valid_bet(self, ctx):
        while True:
            self.current_bet = await self.wait_for_bet_message(ctx)
            if await self.bet_validator.is_bet_permitted(self.current_bet):
                self.current_bet = BetFactory.create_bet(int(self.current_bet.content), ctx.author.id)
                return self.current_bet
            if await self.game_validator.is_quitting(self.current_bet):
                await self.game_messenger.send_quit_game_message()
                return None

    async def wait_for_bet_message(self, ctx):
        try:
            return await self.bot.wait_for(
                'message',
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
        except asyncio.TimeoutError:
            await self.game_messenger.send_bet_timeout()
            return None

    @abstractmethod
    async def start_game(self):
        raise NotImplementedError("This method should be overridden by subclasses.")