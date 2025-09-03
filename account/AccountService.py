from account.Account import Account
from account import AccountRepository


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def get_account(self, user_id: int) -> Account:
        return self.repository.load_account(user_id)

    def create_account(self, user_id: int) -> Account:
        account = Account(user_id)
        self.repository.save(account)
        return account

    def add_daily_reward_to_user(self, account: Account) -> None:
        account.add_coins(10)
        self.save_account(account)

    def save_account(self, account: Account) -> None:
        self.repository.save(account)

    def get_all_accounts(self) -> list[Account]:
        return self.repository.accounts
    

    def reset_daily_claims(self) -> None:
        accounts = self.get_all_accounts()
        for account in accounts:
            account.reset_daily_claim()
        self.repository.save_all(accounts)

    
