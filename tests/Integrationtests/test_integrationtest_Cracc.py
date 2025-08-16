import discord
import pytest
from unittest.mock import AsyncMock, MagicMock
from cogs.AccountCommands import AccountCommands
from discord.ext import commands
@pytest.mark.asyncio
class TestCraccIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.ctx = MagicMock()
        self.ctx.send = AsyncMock()
        self.ctx.author.id = 123
        self.ctx.author.mention = "@TestUser"


        self.mock_coin_transfer = MagicMock()
        self.mock_coin_storage = MagicMock()
        self.mock_daily_storage = MagicMock()

        self.cog = AccountCommands(
            bot=MagicMock(),
            coin_transfer=self.mock_coin_transfer,
            coin_storage=self.mock_coin_storage,
            daily_storage=self.mock_daily_storage
        )

    async def test_user_already_has_account(self):
        # Arrange
        self.mock_coin_storage.exists.return_value = True

        # Act
        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("cracc")
        await command.callback(self.cog, self.ctx)

        # Assert
        self.ctx.send.assert_awaited_once_with(
            "@TestUser, Du hast bereits ein Konto."
        )

    async def test_creates_new_account(self):
        self.mock_coin_storage.exists.return_value = False
        self.mock_coin_transfer.get_starting_coins.return_value = 100

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("cracc")
        await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_awaited_once_with(
            "@TestUser, Dein Konto wurde erfolgreich erstellt!"
        )