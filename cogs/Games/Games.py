"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
import asyncio

from discord.ext import commands


class Game(commands.Cog):

    def __init__(self, bot, coin_storage):
        super().__init__()
        self.bot = bot
        self.coin_storage = coin_storage

    async def asking_for_bet(self, ctx, minimum_bet=10, maximum_bet=1000):
        if not await self.has_account(ctx):
            await ctx.send(f"{ctx.author.mention}, du hast kein Konto. Erstelle ein Konto mit !cracc, um das Spiel zu starten.")
            return None
        if self.does_player_have_enough_coins(ctx, minimum_bet):
            await ctx.send(f"{ctx.author.mention}, du hast nicht genug Coins, um das Spiel zu starten. "
                           f"Du benötigst mindestens {minimum_bet} coins."
                           f"\n\ndein aktueller Kontostand: {self.coin_storage.get(ctx.author.id)}")
            return None
        await ctx.send(f"{ctx.author.mention}, bitte gib deinen Einsatz(minimum=10 und maximum=1000) an, um das Spiel zu starten.")
        return await self.get_valid_bet(ctx, maximum_bet, minimum_bet)

    def does_player_have_enough_coins(self, ctx, minimum_bet):
        return self.coin_storage.get(ctx.author.id) < minimum_bet

    async def get_valid_bet(self, ctx, maximum_bet, minimum_bet):
        while True:
            bet = await self.get_bet(ctx)
            if await self.is_bet_legit(bet, maximum_bet, minimum_bet):
                await ctx.send(f"Dein Einsatz von {bet.content} coins wurde akzeptiert. Viel Glück!")
                return int(bet.content)
            if bet.content.lower() == 'abbrechen':
                await ctx.send("Spiel abgebrochen.")
                return None
            await self.handle_bet_with_responses(bet, ctx, maximum_bet, minimum_bet)

    async def handle_bet_with_responses(self, bet, ctx, maximum_bet, minimum_bet):
        if await self.is_bet_negative(bet):
            await ctx.send("Der Einsatz muss eine positive Zahl sein.")
        elif await self.is_bet_too_high(bet, maximum_bet):
            await ctx.send(f"Der Einsatz darf nicht höher als {maximum_bet} sein.")
        elif await self.is_bet_too_low(bet, minimum_bet):
            await ctx.send(f"Der Einsatz muss mindestens {minimum_bet} coins betragen.")
        elif await self.is_bet_affordable(bet):
            await ctx.send(f"Du hast nicht genug Coins. "
                           f"Dein Kontostand ist {self.coin_storage.get(bet.author.id)} coins.")
        else:
            await ctx.send("Ungültiger Einsatz.")



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

    async def has_account(self, ctx):
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

    async def is_bet_legit(self, bet, maximum_bet, minimum_bet):
        return (bet.content.isdigit()
                and int(bet.content) > 0
                and minimum_bet <= int(bet.content) <= maximum_bet
                and self.coin_storage.get(bet.author.id) >= int(bet.content))

    def start_game(self):
        """
        This method should be overridden by subclasses to implement game-specific logic.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")