


from cogs.Games import BetValidator


class GuessingGameMessenger:
    def __init__(self, channel, bet_validator: BetValidator):
        self.channel = channel
        self.bet_validator = bet_validator

    async def send_game_intro_message(self, ctx):
        await self.channel.send(f"{ctx.author.mention}, ich denke an eine Zahl zwischen 1 und 100. "
                                "Versuche sie zu erraten! Du hast 30 Sekunden Zeit, um deine Antwort zu geben und nur 3 Versuche.")
        
    async def send_invalid_guess_message(self, guess, number_to_guess):
        if not self.bet_validator:
            await self.channel.send("Bitte gib eine Zahl zwischen 1 und 100 ein.")
        if self.is_smaller(guess, number_to_guess):
            await self.channel.send("Zu niedrig!")
        if self.is_greater(guess, number_to_guess):
            await self.channel.send("Zu hoch!")

    async def send_game_over_message(self, number_to_guess):
        await self.channel.send(f"Das Spiel ist vorbei! Die Zahl war {number_to_guess}.")

    async def send_win_game_message(self, bet, author_mention, number_to_guess):
        await self.channel.send(f"Glückwunsch {author_mention}! Du hast die Zahl {number_to_guess} erraten und {bet} coins gewonnen!")

    async def send_three_attempts_over_message(self, number_to_guess):
        await self.channel.send(f"Du hast deine 3 Versuche aufgebraucht! Die Zahl war {number_to_guess}.")

    