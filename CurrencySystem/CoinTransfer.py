from FileOperations import CoinsFileOperations


class CoinTransfer:
    def __init__(self):
        self.coins_file_path = '/files/coins.yaml'
        self.user_file = CoinsFileOperations(self.coins_file_path)
        self.users_coins = self.user_file.load_file().get('users', {})

    def add_coins(self, user_id: str, amount):
        if not self.is_in_databank(user_id):
            self.initialize_account(user_id)
        self.increase_coins(amount, user_id)

    def initialize_account(self, user_id):
        self.users_coins[user_id] = 100
        self.user_file.write_file(self.users_coins)
        self.save_coins()

    def increase_coins(self, amount, user_id):
        self.users_coins[user_id] += amount
        self.save_coins()

    def remove_coins(self, user_id, amount):
        if not self.is_in_databank(user_id):
            raise ValueError(f"Nutzer ist nicht in der Datenbank.")
        self.decrease_coins(amount, user_id)


    def user_cannot_afford_that(self, amount, user_id):
        return not self.is_affordable(amount, user_id)


    def decrease_coins(self, amount, user_id):
        self.users_coins[user_id] -= amount
        if self.is_account_negative(user_id):
            self.set_account_to_zero(amount, user_id)
        self.save_coins()


    def is_account_negative(self, user_id):
        return self.users_coins[user_id] < 0


    def set_account_to_zero(self, amount, user_id):
        self.users_coins[user_id] = 0
        raise ValueError(f"Du hast nicht genug um {amount} coins zu begleichen, "
                         f"dein Kontostand wird auf 0 gesetzt..")


    def is_affordable(self, amount, user_id):
        return self.users_coins[user_id] >= amount


    def is_in_databank(self, user_id):
        if not self.users_coins:
            return False
        return user_id in self.users_coins


    def save_coins(self):
        coins_file = CoinsFileOperations(self.coins_file_path)
        coins_file.write_file(self.users_coins)

    def get_coins(self, user_id):
        if not self.is_in_databank(user_id):
            raise ValueError(f"Nutzer ist nicht in der Datenbank.")
        return self.users_coins[user_id]