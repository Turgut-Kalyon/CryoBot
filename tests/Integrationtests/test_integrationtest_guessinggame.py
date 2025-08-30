from unittest.mock import MagicMock, AsyncMock, patch
import discord
import pytest
from discord.ext import commands
from cogs.Games.GuessingGame import GuessingGame


@pytest.mark.asyncio
class TestGuessingGameIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.ctx = AsyncMock()
        self.ctx.send = AsyncMock()
        self.ctx.author.id = 123
        self.ctx.author.mention = "@TestUser"


        self.cog = GuessingGame(
            bot=MagicMock(),
            coin_storage=MagicMock(),
            coin_transfer=MagicMock()
        )

    async def test_valid_bet(self):
        self.cog.asking_for_bet = AsyncMock(return_value=10)
        self.cog.is_bet_valid = AsyncMock(return_value=True)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("guess")
        await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_awaited_with(
            "@TestUser, ich denke an eine Zahl zwischen 1 und 100. "
            "Versuche sie zu erraten! Du hast 30 Sekunden Zeit, um deine Antwort zu geben und nur 3 Versuche."
        )

    async def test_invalid_bet(self):
        self.cog.asking_for_bet = AsyncMock(return_value=None)
        self.cog.is_bet_valid = AsyncMock(return_value=False)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("guess")
        await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_not_awaited_with(
            "@TestUser, ich denke an eine Zahl zwischen 1 und 100. "
            "Versuche sie zu erraten! Du hast 30 Sekunden Zeit, um deine Antwort zu geben und nur 3 Versuche."
        )


    async def test_win_game(self):
        self.cog.is_bet_valid = AsyncMock(return_value=True)
        self.cog.get_player_answer = AsyncMock(return_value=50)
        self.cog.get_guess_feedback = AsyncMock(return_value="")
        self.cog.win_game = AsyncMock()
        self.cog.play_guessing_round = AsyncMock()


        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        with patch("cogs.Games.GuessingGame.randint", return_value=50):
            command = bot.get_command("guess")
            await command.callback(self.cog, self.ctx)

        self.cog.win_game.assert_awaited_once()
        self.ctx.send.assert_awaited_with(
            "Glückwunsch @TestUser! Du hast die Zahl 50 erraten!"
        )

    async def test_lose_game(self):
        self.cog.is_bet_valid = AsyncMock(return_value=True)
        self.cog.get_player_answer = AsyncMock(return_value=50)
        self.cog.get_guess_feedback = AsyncMock(return_value="Zu niedrig!")
        self.cog.is_game_over = AsyncMock(return_value=True)
        self.cog.lose_game = AsyncMock()
        self.cog.play_guessing_round = AsyncMock()

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        with patch("cogs.Games.GuessingGame.randint", return_value=75):
            command = bot.get_command("guess")
            await command.callback(self.cog, self.ctx)

        self.cog.lose_game.assert_awaited_once()
        self.ctx.send.assert_awaited_with(
            "Du hast deine 3 Versuche aufgebraucht! Die Zahl war 75."
        )