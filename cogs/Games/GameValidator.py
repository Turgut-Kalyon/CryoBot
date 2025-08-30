from cogs.Games.Games import Validator


class GameValidator(Validator):

    def __init__(self, coin_storage, minimum_bet, maximum_bet):
        super().__init__(coin_storage, minimum_bet, maximum_bet)
    
    @staticmethod
    def is_game_over(attempts: int) -> bool:
        return attempts > 3

    def is_guess_in_range(self, guess: int) -> bool:
        return guess < 101 and guess > 0

    def has_account(self, ctx):
        return self.coin_storage.exists(ctx.author.id)
    
    def has_enough_coins(self, ctx):
        return self.coin_storage.get(ctx.author.id) >= self.minimum_bet
    
    async def is_player_eligible_to_play(self, ctx):
        if not self.has_account(ctx):
            await self.send_no_account_message(ctx)
            return False
        if not self.has_enough_coins(ctx):
            await self.send_can_not_afford_message(ctx)
            return False
        return True
    
    async def is_quitting(self, bet):
        return bet.content.lower() == 'abbrechen'