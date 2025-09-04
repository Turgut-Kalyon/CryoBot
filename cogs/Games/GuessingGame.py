from random import randint
from discord.ext import commands
from account import AccountService
from cogs.Games.Games import Game
from Messenger.GuessingGame_Messenger import GuessingGameMessenger 


class GuessingGame(Game):
    """
    A simple guessing game where the user has to guess a number.
    """

    def __init__(self, bot, account_service: AccountService):
        super().__init__(bot, account_service, 2, 150)
        self.messenger = GuessingGameMessenger(bot.channel, self.bet_validator)
        self.number_to_guess: int = None
        self.is_game_won: bool = False

    @commands.command(name='guess', help="!guess", description="Start a guessing game where you have to guess a number between 1 and 100.")
    async def start_game(self, ctx):
        self.current_bet = await self.asking_for_bet(ctx)
        if not self.bet_validator.is_bet_permitted(self.current_bet.amount):
            return
        self.messenger.send_game_intro_message(ctx)
        self.initialize_guessing_number()
        self.is_game_won = False
        await self.play_guessing_round(ctx, 1)

    def initialize_guessing_number(self):
        self.number_to_guess = randint(1, 100)


    async def play_guessing_round(self, ctx, n_attempts):
        while not self.game_validator.is_game_over(n_attempts):
            n_attempts = self.increase_attempts(n_attempts)
            await self.process_guessing_attempt(ctx)
            if self.is_game_won:
                return
        self.account_service.lose_game(ctx.author.id, self.current_bet)
        await self.messenger.send_three_attempts_over_message(ctx.author.mention, self.number_to_guess)

    async def process_guessing_attempt(self, ctx):
        guess = await self.get_player_answer(ctx)
        await self.messenger.send_invalid_guess_message(guess, self.number_to_guess) # TODO: Implementiere die Methode
        if guess == self.number_to_guess:
            await self.win_game(ctx)
            return

    @staticmethod
    def increase_attempts(attempts: int) -> int:
        return attempts + 1


    async def win_game(self, ctx) -> None:
        prize = self.current_bet.amount * 1.3
        self.account_service.win_game(ctx.author.id, prize)
        await self.messenger.send_win_game_message(prize, ctx.author.mention, self.number_to_guess)
        self.is_game_won = True



    async def get_player_answer(self, ctx) -> int:
        answer = await self.bot.wait_for(
            'message',
            timeout=30.0,
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )
        return int(answer.content)
