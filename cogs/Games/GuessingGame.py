from random import randint

from discord.ext import commands

from cogs.Games.Games import Game


class GuessingGame(Game):
    """
    A simple guessing game where the user has to guess a number.
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.coin_transfer = bot.coin_transfer

    @commands.command(name='guess', help="!guess", description="Start a guessing game where you have to guess a number between 1 and 100.")
    async def start_game(self, ctx):
        bet: int = await self.asking_for_bet(ctx)
        await ctx.send(f"{ctx.author.mention}, ich denke an eine Zahl zwischen 1 und 100. "
                       "Versuche sie zu erraten! Du hast 30 Sekunden Zeit, um deine Antwort zu geben und nur 3 Versuche.")
        number_to_guess = randint(1, 100)
        attempts: int = 0


        while not self.is_game_over(attempts):
            try:
                attempts: int = self.increase_attemps(attempts)
                guess: int = await self.get_player_answer(ctx)
                message: str = self.handle_guess(guess, number_to_guess)
                if message:
                    await ctx.send(message)
                    continue
                await self.win_game(bet, ctx, number_to_guess)
                return
            except ValueError:
                await ctx.send("Das ist keine gültige Zahl. Bitte versuche es erneut.")
            except Exception as e:
                await ctx.send(f"Ein Fehler ist aufgetreten: {e}")
        await self.lose_game(bet, ctx, number_to_guess)

    async def lose_game(self, bet, ctx, number_to_guess):
        await ctx.send(f"Du hast deine 3 Versuche aufgebraucht! Die Zahl war {number_to_guess}.")
        self.bot.coin_transfer.remove_coins(ctx.author.id, bet)

    @staticmethod
    def increase_attemps(attempts: int) -> int:
        return attempts + 1

    @staticmethod
    async def win_game(bet, ctx, number_to_guess) -> None:
        bet *= 1.3
        await ctx.send(f"Du hast {bet} coins gewonnen!")
        ctx.bot.coin_transfer.add_coins(ctx.author.id, bet)
        await ctx.send(f"Glückwunsch {ctx.author.mention}! Du hast die Zahl {number_to_guess} erraten!")

    def handle_guess(self, guess, number_to_guess) -> str:
        if not self.is_guess_valid(guess):
            return "Bitte gib eine Zahl zwischen 1 und 100 ein."
        if self.is_smaller(guess, number_to_guess):
            return "Zu niedrig!"
        if self.is_greater(guess, number_to_guess):
            return "Zu hoch!"
        return ""

    @staticmethod
    def is_greater(guess, number_to_guess) -> bool:
        return guess > number_to_guess

    @staticmethod
    def is_smaller(guess, number) -> bool:
        return guess < number

    def is_guess_valid(self, guess) -> bool:
        return self.is_smaller(guess,100) or self.is_greater(guess,1)

    async def get_player_answer(self, ctx) -> int:
        answer = self.bot.wait_for(
            'message',
            timeout=30.0,
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )
        return int(answer.content)

    @staticmethod
    def is_game_over(attempts: int) -> bool:
        return attempts > 3



