import discord
import pytest
from unittest.mock import AsyncMock, MagicMock

from discord.ext.commands import MissingPermissions

from cogs.CustomTextCommandCog import CustomTextCommandCog
from discord.ext import commands
@pytest.mark.asyncio
class TestCustomCmdIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.ctx = AsyncMock()
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

    async def test_remove_command_admin_permissions(self):
        # Test removing a custom command without admin permissions
        self.ctx.author.guild_permissions.administrator = False

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("removecommand")
        with pytest.raises(MissingPermissions):
            await command.invoke(self.ctx)

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
        self.cog.has_no_parameters_given = MagicMock(return_value=False)
        self.cog.is_command_already_existing = MagicMock(return_value=True)
        self.cog.get_command_name = MagicMock(return_value="This is a custom command")

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("execCommand")
        await command.callback(self.cog, self.ctx, "test")

        self.ctx.send.assert_awaited_once_with("This is a custom command")

    async def test_exec_non_existing_custom_command(self):
        # Test executing a non-existing custom command
        self.ctx.message.content = "!execCommand test"
        self.cog.is_command_already_existing = MagicMock(return_value=False)
        self.cog.has_no_parameters_given = MagicMock(return_value=False)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("execCommand")
        await command.callback(self.cog, self.ctx, "test")

        self.ctx.send.assert_awaited_once_with(
            "Es gibt keinen Befehl mit dem Namen: 'test'. "
            "Bitte überprüfe den Befehl und versuche es erneut "
            "ODER erstelle einen Befehl mit diesem Namen."
        )

    async def test_exec_command_no_parameters(self):
        # Test executing a command with no parameters
        self.ctx.message.content = "!execCommand"
        self.cog.has_no_parameters_given = MagicMock(return_value=True)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("execCommand")
        await command.callback(self.cog, self.ctx)

        self.ctx.send.assert_awaited_once_with("Gib einen Befehlnamen ein SOFORT!!!")


    async def test_add_command_with_admin(self):
        self.ctx.author.guild_permissions.administrator = True
        self.cog.has_no_parameters_given = MagicMock(return_value=False)
        self.cog.is_command_already_existing = MagicMock(return_value=False)

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("addcommand")
        await command.callback(self.cog, self.ctx, "test", response="Hallo")

        self.mock_cmd_storage.set.assert_called_once_with("test", "Hallo")
        self.ctx.send.assert_awaited_once_with("Befehl 'test' wurde erfolgreich hinzugefügt.")

    async def test_add_command_without_admin(self):
        self.ctx.author.guild_permissions.administrator = False

        bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        await bot.add_cog(self.cog)

        command = bot.get_command("addcommand")

        with pytest.raises(MissingPermissions):
            await command.invoke(self.ctx)

    async def test_has_no_parameters_given(self):
        assert self.cog.has_no_parameters_given("", "") is True
        assert self.cog.has_no_parameters_given("test", "") is True
        assert self.cog.has_no_parameters_given("", "response") is True
        assert self.cog.has_no_parameters_given("test", "response") is False
        assert self.cog.has_no_parameters_given("test", "no parameter given") is False
        assert self.cog.has_no_parameters_given("", "no parameter given") is True


