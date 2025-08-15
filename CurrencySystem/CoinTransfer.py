from Storage import Storage


class CoinTransfer:
    def __init__(self, storage: Storage):
        self.coin_storage = storage
        self.starting_coins = 10

    def add_coins(self, user_id: str, amount):
        if not self.coin_storage.exists(user_id):
            return
        self.coin_storage.adjust(user_id, amount)
    def remove_coins(self, user_id, amount):
        if not self.coin_storage.exists(user_id):
            return
        self.coin_storage.adjust(user_id, -amount)

    def get_coins(self, user_id):
        if not self.coin_storage.exists(user_id):
            return None
        return self.coin_storage.get(user_id)

    @property
    def get_starting_coins(self):
        return self.starting_coins