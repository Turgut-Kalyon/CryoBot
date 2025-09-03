from account.Account import Account
from Storage import Storage

class AccountRepository:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.accounts = self.load_all()


    def save(self, account: Account) -> None:
        data = {
            "coins": account.balance,
            "games_won": account.games_won,
            "games_lost": account.games_lost,
            "games_total": account.games_total,
            "daily_claimed": account.has_claimed_daily
        }
        self.accounts[account.id] = account
        self.storage.set(str(account.id), data)

    def load_account(self, user_id: int) -> Account:
        data = self.storage.get(str(user_id))
        if not data:
            return Account(user_id, initial_coins=10.0)
        acc = Account(user_id, initial_coins=data["coins"])
        acc.game_statistics = {
            "games_won": data["games_won"],
            "games_lost": data["games_lost"],
            "games_total": data["games_total"]
        }
        acc.daily_claimed = data["daily_claimed"]
        return acc

    def load_all(self) -> list[Account]:
        accounts = []
        for user_id, data in self.storage.yaml_file[self.storage.main_key].items():
            acc = Account(int(user_id), initial_coins=data["coins"])
            acc.game_statistics = data["game_statistics"]
            acc.daily_claimed = data["daily_claimed"]
            accounts.append(acc)
        return accounts

    def save_all(self, accounts: list[Account]) -> None:
        for acc in accounts:
            self.save(acc)

    

    @property
    def accounts(self) -> list[Account]:
        return list(self.accounts.values())