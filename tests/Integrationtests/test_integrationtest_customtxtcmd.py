import discord
import pytest
from unittest.mock import AsyncMock, MagicMock
from cogs.CustomTextCommandCog import CustomTextCommandCog
from discord.ext import commands
@pytest.mark.asyncio
class TestCustomCmdIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.ctx = MagicMock()
        self.ctx.send = AsyncMock()
        self.ctx.author.id = 123
        self.ctx.author.mention = "@TestUser"


        self.mock_cmd_storage = MagicMock()
        self.mock_cmd_storage.set = MagicMock()

        self.cog = CustomTextCommandCog(
            bot=MagicMock(),
            storage= self.mock_cmd_storage
        )

    async def test_add_custom_command_w_parameters(self):
        # Test adding a custom command with parameters
        self.ctx.message.content = "!addcommand test This is a custom command"
        self.cog.has_no_parameters_given = MagicMock(return_value=False)
        self.cog.is_command_already_existing = MagicMock(return_value=False)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("addcommand")
        await command.callback(self.cog, self.ctx, "test", response="This is a custom command")

        self.mock_cmd_storage.set.assert_called_once_with("test", "This is a custom command")
        self.ctx.send.assert_awaited_once_with(
            "Befehl 'test' wurde erfolgreich hinzugefügt."
        )

    async def test_add_custom_command_no_parameters(self):
        # Test adding a custom command with no parameters
        self.ctx.message.content = "!addcommand test"
        self.cog.has_no_parameters_given = MagicMock(return_value=True)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("addcommand")
        await command.callback(self.cog, self.ctx, "test")

        self.ctx.send.assert_awaited_once_with(
            "Befehlsname und Antwort dürfen nicht leer sein."
        )

    async def test_add_custom_command_already_exists(self):
        # Test adding a custom command that already exists
        self.ctx.message.content = "!addcommand test This is a custom command"
        self.cog.has_no_parameters_given = MagicMock(return_value=False)
        self.cog.is_command_already_existing = MagicMock(return_value=True)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("addcommand")
        await command.callback(self.cog, self.ctx, "test", response="This is a custom command")

        self.ctx.send.assert_awaited_once_with(
            "Befehl 'test' existiert bereits. Bitte wähle einen anderen Namen."
        )

    async def test_remove_existing_custom_command(self):
        # Test removing a custom command
        self.ctx.message.content = "!removecommand test"
        self.cog.is_command_already_existing = MagicMock(return_value=True)
        self.mock_cmd_storage.delete = MagicMock()

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("removecommand")
        await command.callback(self.cog, self.ctx, "test")

        self.mock_cmd_storage.delete.assert_called_once_with("test")
        self.ctx.send.assert_awaited_once_with(
            "Befehl 'test' wurde erfolgreich entfernt."
        )

    async def test_remove_non_existing_custom_command(self):
        # Test removing a custom command that does not exist
        self.ctx.message.content = "!removecommand test"
        self.cog.is_command_already_existing = MagicMock(return_value=False)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("removecommand")
        await command.callback(self.cog, self.ctx, "test")

        self.ctx.send.assert_awaited_once_with(
            "Befehl 'test' existiert nicht. Bitte überprüfe den Befehl und versuche es erneut."
        )

    async def test_exec_existing_custom_command(self):
        # Test executing an existing custom command
        self.ctx.message.content = "!execCommand test"
        self.cog.is_command_already_existing = MagicMock(return_value=True)
        self.cog.get_command_name = MagicMock(return_value="This is a custom command")

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("execCommand")
        await command.callback(self.cog, self.ctx, "test")

        self.ctx.send.assert_awaited_once_with("This is a custom command")



