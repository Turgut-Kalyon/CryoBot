from unittest.mock import MagicMock, AsyncMock
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

        self.mock_coin_transfer = MagicMock()

        self.cog = GuessingGame(
            bot=MagicMock(),
        )

    async def test_start_guessing_game(self):
        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("guess")
        await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_awaited_once_with(
            "Das Ratespiel wurde gestartet! Rate eine Zahl zwischen 1 und 100."
        )