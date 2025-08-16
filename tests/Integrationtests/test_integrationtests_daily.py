from datetime import datetime

import discord
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from cogs.DailyCoins import DailyCoins


@pytest.mark.asyncio
class TestDailyIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.ctx = MagicMock()
        self.ctx.send = AsyncMock()
        self.ctx.author.id = 123
        self.ctx.author.mention = "@TestUser"

        self.mock_coin_transfer = MagicMock()
        self.mock_daily_storage = MagicMock()

        self.cog = DailyCoins(
            bot=MagicMock(),
            coin_transfer=self.mock_coin_transfer,
            storage=self.mock_daily_storage
        )

    async def test_has_no_account(self):
        self.mock_daily_storage.exists.return_value = False

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        with patch("cogs.DailyCoins.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 0, 0)
            mock_datetime.time = datetime.time
            command = bot.get_command("daily")
            await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_awaited_once_with(
            "@TestUser, Du hast noch kein Konto. Erstelle ein Konto mit !cracc, um tägliche Coins zu erhalten."
        )

    async def test_received_daily_reward(self):
        self.mock_daily_storage.exists.return_value = True
        self.mock_daily_storage.get.return_value = "12:00:00"

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        with patch("cogs.DailyCoins.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 0, 0)
            mock_datetime.time = datetime.time
            command = bot.get_command("daily")
            await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_awaited_once_with(
            "Du hast deine täglichen Coins bereits abgeholt. "
            "Du kannst sie jeden Tag um 00:00 Uhr abholen."
        )

    async def test_adds_daily_reward(self):
        self.mock_daily_storage.exists.return_value = True
        self.mock_daily_storage.get.return_value = None

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        with patch("cogs.DailyCoins.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 0, 0)
            mock_datetime.time = datetime.time
            command = bot.get_command("daily")
            await command.callback(self.cog, self.ctx)

        self.mock_coin_transfer.add_coins.assert_called_once_with(123, 10)
        self.mock_daily_storage.set.assert_called_once_with(123, "00:00:00")

        self.ctx.send.assert_awaited_once_with(
            "@TestUser hat 10 coins bekommen."
        )


    async def test_clear_yaml_task_at_midnight(self):
        with patch("cogs.DailyCoins.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 0, 0)
            mock_datetime.time = datetime.time
            await self.cog.clear_yaml_task()

        self.mock_daily_storage.set_all.assert_called_once_with(None)

    async def test_clear_yaml_task_not_midnight(self):
        with patch("cogs.DailyCoins.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 11, 0)
            mock_datetime.time = datetime.time
            await self.cog.clear_yaml_task()

        self.mock_daily_storage.set_all.assert_not_called()