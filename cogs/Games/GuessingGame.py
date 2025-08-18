from random import randint

from cogs.Games.Games import Game


class GuessingGame(Game):
    """
    A simple guessing game where the user has to guess a number.
    """

    def __init__(self, bot):
        super().__init__(bot)

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



