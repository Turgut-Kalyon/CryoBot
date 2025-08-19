"""
Author: Turgut Kalyon
Description: Game module for CryoBot, providing a base class for game-related functionalities.
"""
from discord.ext import commands
from random import randint


class Game(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def asking_for_bet(self, ctx, minimum_bet=10, maximum_bet=1000):
        ctx.send(f"{ctx.author.mention}, bitte gib deinen Einsatz(minimum=10 und maximum=1000) an, um das Spiel zu starten.")
        while True:
            bet = await self.bot.wait_for(
                'message',
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            if self.is_bet_legit(bet, maximum_bet, minimum_bet):
                await ctx.send(f"Dein Einsatz von {bet.content} coins wurde akzeptiert. Viel Glück!")
                return int(bet.content)
            await ctx.send("Ungültiger Einsatz. Bitte gib eine positive Zahl ein.")

    def is_bet_legit(self, bet, maximum_bet, minimum_bet):
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

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name='guess', help="!guess", description="Start a guessing game where you have to guess a number between 1 and 100.")
    async def start_game(self, ctx):
        bet = await self.asking_for_bet(ctx)
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



