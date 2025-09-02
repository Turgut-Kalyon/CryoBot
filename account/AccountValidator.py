
from account.Account import Account


class AccountValidator:

    def __init__(self, accounts: list[Account]):
        self.accounts = accounts

    def has_account(self, user_id: int) -> bool:
        return any(user.id == user_id for user in self.accounts)
