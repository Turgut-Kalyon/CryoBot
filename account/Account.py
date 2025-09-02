


class Account:
    def __init__(self, user_id: int, initial_coins: float = 10.0):
        self.user_id = user_id
        self.coins = initial_coins
        self.game_statistics = {
            "games_won": 0,
            "games_lost": 0,
            "games_total": 0
        }
        self.daily_claimed = False

    def can_afford(self, amount: float) -> bool:
        return self.coins >= amount

    def win_game(self, coins: float) -> None:
        self.game_statistics["games_won"] += 1
        self.coins += coins

    def lose_game(self, coins: float) -> None:
        self.game_statistics["games_lost"] += 1
        self.coins -= coins

    def reset_daily_claim(self):
        self.daily_claimed = False

    @property
    def id(self) -> int:
        return self.user_id

    @property
    def has_claimed_daily(self) -> bool:
        return self.daily_claimed

    @property
    def balance(self) -> float:
        return self.coins

    @property
    def games_won(self) -> int:
        return self.game_statistics["games_won"]

    @property
    def games_lost(self) -> int:
        return self.game_statistics["games_lost"]

    @property
    def games_total(self) -> int:
        return self.game_statistics["games_total"]


