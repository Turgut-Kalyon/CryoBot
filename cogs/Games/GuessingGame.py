from random import randint
from discord.ext import commands
from cogs.Games.Games import Game
from Messenger.GuessingGame_Messenger import GuessingGameMessenger  # Add this import if GuessingGameMessenger is defined in this module


class GuessingGame(Game):
    """
    A simple guessing game where the user has to guess a number.
    """

    def __init__(self, bot):
        super().__init__(bot, 2, 150)
        self.messenger = GuessingGameMessenger(bot.channel, self.bet_validator)

    @commands.command(name='guess', help="!guess", description="Start a guessing game where you have to guess a number between 1 and 100.")
    async def start_game(self, ctx):
        bet, number_to_guess = await self.preparation_for_game(ctx)
        if not await self.is_bet_valid(bet):
            return
        await self.play_guessing_round(bet, ctx, number_to_guess, 1)


    async def preparation_for_game(self, ctx):
        bet: int = await self.asking_for_bet(ctx)
        if not await self.is_bet_valid(bet):
            return None
        await self.messenger.send_game_intro_message(ctx)
        number_to_guess = randint(1, 100)
        return bet, number_to_guess



    async def play_guessing_round(self, bet, ctx, number_to_guess, attempts):
        while not self.is_game_over(attempts):
            attempts = self.increase_attemps(attempts)
            await self.process_guessing_attempt(bet, ctx, number_to_guess)
        await self.lose_game(bet, ctx, number_to_guess)

    async def process_guessing_attempt(self, bet, ctx, number_to_guess):
        guess = await self.get_player_answer(ctx)
        await self.messenger.send_invalid_guess_message(guess, number_to_guess)
        if guess == number_to_guess:
            await self.win_game(bet, ctx, number_to_guess)
        return

    @staticmethod
    async def is_bet_valid(bet):
        return bet is not None

    async def lose_game(self, bet, ctx, number_to_guess):
        await self.messenger.send_three_attempts_over_message(number_to_guess)


    @staticmethod
    def increase_attempts(attempts: int) -> int:
        return attempts + 1

    async def win_game(self, bet, ctx, number_to_guess) -> None:
        bet *= 1.3
        self.coin_transfer.add_coins(ctx.author.id, bet)
        await self.messenger.send_win_game_message(bet, ctx.author.mention, number_to_guess)



    async def get_player_answer(self, ctx) -> int:
        answer = await self.bot.wait_for(
            'message',
            timeout=30.0,
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )
        return int(answer.content)



