from account import Account, AccountRepository


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def get_account(self, user_id: int) -> Account:
        return self.repository.load_account(user_id)

    def save_account(self, account: Account) -> None:
        self.repository.save(account)
