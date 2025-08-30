import Storage


class Validator:
    def __init__(self, coin_storage: Storage, minimum_bet: int, maximum_bet: int):
        self.coin_storage = coin_storage
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
