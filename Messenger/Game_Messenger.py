



from cogs.Games import BetValidator


class GameMessenger:

    def __init__(self, channel, minimum_bet, maximum_bet, bet_validator: BetValidator):
        self.channel = channel
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
        self.bet_validator = bet_validator

    async def send_bet_validation_error(self, current_bet):
        if await self.bet_validator.is_bet_negative(current_bet):
            await self.send_it_has_to_be_positive_number()
        elif await self.bet_validator.is_bet_too_high(current_bet):
            await self.send_bet_is_too_high()
        elif await self.bet_validator.is_bet_too_low(current_bet):
            await self.send_bet_is_too_low()
        else:
            await self.channel.send("Ungültiger Einsatz.")

    async def send_it_has_to_be_positive_number(self):
        await self.channel.send("Der Einsatz muss eine positive Zahl sein.")

    async def send_bet_is_too_low(self):
        await self.channel.send(f"Der Einsatz muss mindestens {self.minimum_bet} coins betragen.")

    async def send_bet_is_too_high(self):
        await self.channel.send(f"Der Einsatz darf nicht höher als {self.maximum_bet} sein.")