"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
from discord.ext import commands
from random import randint


class Game(commands.Cog):

    def __init__(self, bot, coin_storage):
        super().__init__()
        self.bot = bot
        self.coin_storage = coin_storage

    async def asking_for_bet(self, ctx, minimum_bet=10, maximum_bet=1000):
        if not self.has_account(ctx):
            await ctx.send(f"{ctx.author.mention}, du hast kein Konto. Erstelle ein Konto mit !cracc, um das Spiel zu starten.")
            return None
        ctx.send(f"{ctx.author.mention}, bitte gib deinen Einsatz(minimum=10 und maximum=1000) an, um das Spiel zu starten.")
        do:
            bet = await self.get_bet(ctx)
            if self.is_bet_legit(bet, maximum_bet, minimum_bet):
                await ctx.send(f"Dein Einsatz von {bet.content} coins wurde akzeptiert. Viel Glück!")
                return int(bet.content)
            await ctx.send("Ungültiger Einsatz. Bitte gib eine positive Zahl ein.")
        while not self.is_bet_legit(bet, maximum_bet, minimum_bet)

    async def has_account(self, ctx):
        return self.coin_storage.exists(ctx.author.id)

    async def get_bet(self, ctx):
        return self.bot.wait_for(
            'message',
            timeout=30.0,
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )

    @staticmethod
    def is_bet_legit(bet, maximum_bet, minimum_bet):
        return bet.content.isdigit() and int(bet.content) > 0 and minimum_bet <= int(bet.content) <= maximum_bet

    def start_game(self):
        """
        This method should be overridden by subclasses to implement game-specific logic.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

















class GuessingGame(Game):
    """
    A simple guessing game where the user has to guess a number.
    """

    def __init__(self, bot, coin_storage):
        super().__init__(bot, coin_storage)

    @commands.command(name='guess', help="!guess", description="Start a guessing game where you have to guess a number between 1 and 100.")
    async def start_game(self, ctx):
        bet = await self.asking_for_bet(ctx)
        if bet is None:
            return
        await ctx.send(f"{ctx.author.mention}, ich denke an eine Zahl zwischen 1 und 100. "
                       "Versuche sie zu erraten! Du hast 30 Sekunden Zeit, um deine Antwort zu geben und nur 3 Versuche.")
        number_to_guess = randint(1, 100)
        attempts = 0
        while True:
            try:
                attempts += 1
                if attempts > 3:
                    await ctx.send(f"Du hast deine 3 Versuche aufgebraucht! Die Zahl war {number_to_guess}.")
                    break
                guess = await self.bot.wait_for(
                    'message',
                    timeout=30.0,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel
                )

                guess = int(guess.content)
                if guess < 1 or guess > 100:
                    await ctx.send("Bitte gib eine Zahl zwischen 1 und 100 ein. Das ist kein gültiger Versuch.")
                    continue
                if guess < number_to_guess:
                    await ctx.send("Zu niedrig! Versuch es nochmal.")
                elif guess > number_to_guess:
                    await ctx.send("Zu hoch! Versuch es nochmal.")
                else:
                    await ctx.send(f"Glückwunsch {ctx.author.mention}! Du hast die Zahl {number_to_guess} erraten!")
                    break


            except ValueError:
                await ctx.send("Das ist keine gültige Zahl. Bitte versuche es erneut.")
            except Exception as e:
                await ctx.send(f"Ein Fehler ist aufgetreten: {e}")



