from cogs.Games.BetValidator import BetValidator


class GameMessenger:

    def __init__(self, minimum_bet, maximum_bet, bet_validator: BetValidator):
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
        self.bet_validator = bet_validator

    async def send_bet_validation_error(self, ctx, current_bet):
        if self.bet_validator.is_bet_negative(current_bet):
            await self.send_it_has_to_be_positive_number(ctx)
        elif self.bet_validator.is_bet_too_high(current_bet):
            await self.send_bet_is_too_high(ctx)
        elif self.bet_validator.is_bet_too_low(current_bet):
            await self.send_bet_is_too_low(ctx)
        else:
            await ctx.send("Ungültiger Einsatz.")

    async def send_it_has_to_be_positive_number(self, ctx):
        await ctx.send("Der Einsatz muss eine positive Zahl sein.")

    async def send_bet_is_too_low(self, ctx):
        await ctx.send(f"Der Einsatz muss mindestens {self.minimum_bet} coins betragen.")

    async def send_bet_is_too_high(self, ctx):
        await ctx.send(f"Der Einsatz darf nicht höher als {self.maximum_bet} sein.")

    async def send_bet_timeout(self, ctx):
        await ctx.send("Zeitüberschreitung: Du hast zu lange gebraucht, um deinen Einsatz zu nennen.")

    async def send_quit_game_message(self, ctx):
        await ctx.send("Das Spiel wurde beendet.")