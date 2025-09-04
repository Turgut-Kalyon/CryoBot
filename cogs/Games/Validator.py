from account.AccountService import AccountService


class Validator:
    def __init__(self, account_service: AccountService, minimum_bet: int, maximum_bet: int):
        self.account_service = account_service
        self.minimum_bet = minimum_bet
        self.maximum_bet = maximum_bet
