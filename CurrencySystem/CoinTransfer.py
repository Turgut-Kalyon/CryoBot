from Storage import Storage


class CoinTransfer:
    def __init__(self, storage: Storage):
        self.coinsByUser = storage
        self.starting_coins = 10

    def add_coins(self, user_id: str, amount):
        if not self.is_user_existing(user_id):
            return
        self.coinsByUser.adjust(user_id, amount)

    def is_user_existing(self, user_id):
        return self.coinsByUser.exists(user_id)

    def remove_coins(self, user_id, amount):
        if not self.is_user_existing(user_id):
            return
        self.coinsByUser.adjust(user_id, -amount)


    @property
    def get_starting_coins(self):
        return self.starting_coins