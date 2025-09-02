
from cogs.Games.Bet import Bet

class BetFactory:
    @staticmethod
    def create_bet(amount: int, author_id: int) -> Bet:
        return Bet(amount, author_id)