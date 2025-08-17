from discord.ext import commands
from Storage import Storage

DESCR_CMD_NAME = "Name of the command"
DESCR_CMD_RESPONSE = "Response to the command"
description_in_help_commandname = commands.parameter(description=DESCR_CMD_NAME)
description_in_help_response = commands.parameter(description=DESCR_CMD_RESPONSE)

class CustomTextCommandCog(commands.Cog, description="Custom text command handler for CryoBot"):

    @property
    def qualified_name(self):# pragma: no cover
        return "Custom Commands"

    def __init__(self, bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command(name='addcommand',
                      help="!addcommand <command_name> <response>",
                      description="Adds a custom command with a response.")
    @commands.has_permissions(administrator=True)
    async def add_command(self, ctx,
                          command_name: str = description_in_help_commandname, *,
                          response: str = description_in_help_response):
            if self.has_no_parameters_given(command_name, response):
                await ctx.send("Befehlsname und Antwort dürfen nicht leer sein.")
                return
            if self.is_command_already_existing(command_name):
                await ctx.send(f"Befehl '{command_name}' existiert bereits. "
                                 f"Bitte wähle einen anderen Namen.")
                return
            self.storage.set(command_name, response)
            await ctx.send(f"Befehl '{command_name}' wurde erfolgreich hinzugefügt.")


    def is_command_already_existing(self, command_name):# pragma: no cover
        return self.storage.exists(command_name)

    @staticmethod
    def has_no_parameters_given(command_name, response = None):# pragma: no cover
        return not command_name or not response

    @commands.command(name='removecommand',
                      description="Removes a custom command.",
                      help="!removecommand <command_name>")
    @commands.has_permissions(administrator=True)
    async def remove_command(self, ctx,
        command_name: str = commands.parameter(description=DESCR_CMD_NAME)):
            if not self.is_command_already_existing(command_name):
                await ctx.send(f"Befehl '{command_name}' existiert nicht. Bitte überprüfe den Befehl und versuche es erneut.")
                return
            self.storage.delete(command_name)
            await ctx.send(f"Befehl '{command_name}' wurde erfolgreich entfernt.")


    @commands.command(name='execCommand',
                      description="Executes a custom command.",
                      help="!execCommand <command_name>")
    async def exec_command(self, ctx,
        command_name: str = commands.parameter(description=DESCR_CMD_NAME)):
            if self.has_no_parameters_given(command_name):
                await ctx.send("Gib einen Befehlnamen ein SOFORT!!!")
                return
            if not self.is_command_already_existing(command_name):
                await ctx.send(f"Es gibt keinen Befehl mit dem Namen: '{command_name}'. "
                                 f"Bitte überprüfe den Befehl und versuche es erneut "
                                 f"ODER erstelle einen Befehl mit diesem Namen.")
                return
            await ctx.send(self.get_command_name(command_name))

    def get_command_name(self, command_name):# pragma: no cover
        return self.storage.get(command_name)




