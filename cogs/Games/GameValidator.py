

class GameValidator:

    def is_valid_bet_amount(self, bet, min_bet, max_bet):
        if not bet.isdigit():
            return False
        bet = int(bet)
        return min_bet <= bet <= max_bet > 0

    async def is_bet_legit(self, bet, maximum_bet, minimum_bet):
        return (self.is_valid_bet_amount(bet, minimum_bet, maximum_bet)
                and await self.is_bet_affordable(bet))