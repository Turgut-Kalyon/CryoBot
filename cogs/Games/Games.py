"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
import asyncio
from abc import abstractmethod
from discord.ext import commands

#TODO minimum_bet and maximum_bet should be members of the class Game
# and set in the constructor of the subclasses.
# This would make the code cleaner and avoid passing them around in methods.
class Game(commands.Cog):

    def __init__(self, bot, coin_storage):
        super().__init__()
        self.bot = bot
        self.coin_storage = coin_storage

    async def can_player_start_game(self, ctx, minimum_bet):
        if not self.has_account(ctx):
            await self.send_no_account_message(ctx)
            return False
        if not self.has_enough_coins(ctx, minimum_bet):
            await self.send_can_not_afford_message(ctx, minimum_bet)
            return False
        return True

    async def send_no_account_message(self, ctx):
        await ctx.send(
            f"{ctx.author.mention}, du hast kein Konto. Erstelle ein Konto mit !cracc, um das Spiel zu starten.")

    async def send_can_not_afford_message(self, ctx, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, du hast nicht genug Coins, um das Spiel zu starten. "
                       f"Du benötigst mindestens {minimum_bet} coins."
                       f"\n\ndein aktueller Kontostand: {self.coin_storage.get(ctx.author.id)}")

    async def asking_for_bet(self, ctx, minimum_bet=10, maximum_bet=1000):
        if not await self.can_player_start_game(ctx, minimum_bet):
            return None
        await self.send_bet_request_message(ctx, maximum_bet, minimum_bet)
        return await self.get_valid_bet(ctx, maximum_bet, minimum_bet)

    async def send_bet_request_message(self, ctx, maximum_bet, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, bitte gib deinen Einsatz"
                       f"(minimum={minimum_bet} und maximum={maximum_bet}) an, um das Spiel zu starten.")

    def has_enough_coins(self, ctx, minimum_bet):
        return self.coin_storage.get(ctx.author.id) >= minimum_bet

    async def get_valid_bet(self, ctx, maximum_bet, minimum_bet):
        while True:
            bet = await self.get_bet(ctx)
            if await self.is_bet_legit(bet, maximum_bet, minimum_bet):
                await self.send_bet_request_accepted(bet, ctx)
                return int(bet.content)
            if await self.is_quitting(bet):
                await self.send_player_wants_to_quit_the_game(ctx)
                return None
            await self.send_bet_validation_error(bet, ctx, maximum_bet, minimum_bet)

    async def is_quitting(self, bet):
        return bet.content.lower() == 'abbrechen'

    async def send_player_wants_to_quit_the_game(self, ctx):
        await ctx.send("Spiel abgebrochen.")

    async def send_bet_request_accepted(self, bet, ctx):
        await ctx.send(f"Dein Einsatz von {bet.content} coins wurde akzeptiert. Viel Glück!")

    async def send_bet_validation_error(self, bet, ctx, maximum_bet, minimum_bet):
        if await self.is_bet_negative(bet):
            await self.send_it_has_to_be_positive_number(ctx)
        elif await self.is_bet_too_high(bet, maximum_bet):
            await self.send_bet_is_too_high(ctx, maximum_bet)
        elif await self.is_bet_too_low(bet, minimum_bet):
            await self.send_bet_is_too_low(ctx, minimum_bet)
        else:
            await ctx.send("Ungültiger Einsatz.")

    async def send_bet_is_too_low(self, ctx, minimum_bet):
        await ctx.send(f"Der Einsatz muss mindestens {minimum_bet} coins betragen.")

    async def send_bet_is_too_high(self, ctx, maximum_bet):
        await ctx.send(f"Der Einsatz darf nicht höher als {maximum_bet} sein.")

    async def send_it_has_to_be_positive_number(self, ctx):
        await ctx.send("Der Einsatz muss eine positive Zahl sein.")

    async def is_bet_affordable(self, bet):
        return self.coin_storage.get(bet.author.id) >= int(bet.content)

    @staticmethod
    async def is_bet_too_low(bet, minimum_bet):
        return bet.content.isdigit() and int(bet.content) < minimum_bet

    @staticmethod
    async def is_bet_too_high(bet, maximum_bet):
        return bet.content.isdigit() and int(bet.content) > maximum_bet

    @staticmethod
    async def is_bet_negative(bet):
        return bet.content.isdigit() and int(bet.content) <= 0

    def has_account(self, ctx):
        return self.coin_storage.exists(ctx.author.id)

    async def get_bet(self, ctx):
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