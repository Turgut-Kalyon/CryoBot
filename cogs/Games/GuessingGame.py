from random import randint
from discord.ext import commands
from account import Account, AccountRepository
from cogs.Games.Games import Game
from Messenger.GuessingGame_Messenger import GuessingGameMessenger  # Add this import if GuessingGameMessenger is defined in this module


class GuessingGame(Game):
    """
    A simple guessing game where the user has to guess a number.
    """

    def __init__(self, bot, repo: AccountRepository):
        super().__init__(bot, repo, 2, 150)
        self.messenger = GuessingGameMessenger(bot.channel, self.bet_validator)
        self.number_to_guess: int = None

    @commands.command(name='guess', help="!guess", description="Start a guessing game where you have to guess a number between 1 and 100.")
    async def start_game(self, ctx):
        await self.preparation_for_game(ctx)
        if not self.bet_validator.is_bet_permitted(self.current_bet.amount):
            return
        self.initialize_guessing_number()
        await self.play_guessing_round(ctx, 1)


    async def preparation_for_game(self, ctx):
        await self.asking_for_bet(ctx)
        if not self.bet_validator.is_bet_permitted(self.current_bet):
            return None
        await self.messenger.send_game_intro_message(ctx)

    def initialize_guessing_number(self):
        self.number_to_guess = randint(1, 100)


    async def play_guessing_round(self, ctx, n_attempts):
        while not self.is_game_over(n_attempts):
            n_attempts = self.increase_attempts(n_attempts)
            await self.process_guessing_attempt(ctx)
        self.account_service.lose_game(ctx.author.id, self.current_bet)
        await self.messenger.send_three_attempts_over_message()

    async def process_guessing_attempt(self, ctx):
        guess = await self.get_player_answer(ctx)
        await self.messenger.send_invalid_guess_message(guess, self.number_to_guess)
        if guess == self.number_to_guess:
            await self.win_game(ctx)
        return

    @staticmethod
    def increase_attempts(attempts: int) -> int:
        return attempts + 1


    async def win_game(self, ctx) -> None:
        prize = self.current_bet * 1.3
        self.account_service.win_game(ctx.author.id, prize)
        await self.messenger.send_win_game_message(prize, ctx.author.mention, self.number_to_guess)



    async def get_player_answer(self, ctx) -> int:
        answer = await self.bot.wait_for(
            'message',
            timeout=30.0,
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )
        return int(answer.content)



