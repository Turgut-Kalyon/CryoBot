from cogs.Games import Validator, Bet
import Storage

class BetValidator(Validator):
    def __init__(self, coin_storage: Storage, minimum_bet: int, maximum_bet: int):
        super().__init__(coin_storage, minimum_bet, maximum_bet)

    def is_bet_amount_in_range(self, bet: Bet) -> bool:
        return self.minimum_bet <= bet.amount <= self.maximum_bet

    def is_bet_permitted(self, bet: Bet) -> bool:
        return (self.is_bet_amount_in_range(bet)
                and self.is_bet_within_budget(bet))

    def is_bet_within_budget(self, bet: Bet) -> bool:
        return self.coin_storage.get(bet.author_id) >= bet.amount

    def is_bet_too_low(self, bet: Bet) -> bool:
        return bet.amount < self.minimum_bet

    def is_bet_too_high(self, bet: Bet) -> bool:
        return bet.amount > self.maximum_bet

    def is_bet_negative(self, bet: Bet) -> bool:
        return bet.amount <= 0