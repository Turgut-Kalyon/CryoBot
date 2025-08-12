from discord.ext import commands
from Storage import Storage

DESCR_CMD_NAME = "Name of the command"
DESCR_CMD_RESPONSE = "Response to the command"


class CustomTextCommandCog(commands.Cog, description="Custom text command handler for CryoBot"):

    @property
    def qualified_name(self):
        return "Custom Commands"

    def __init__(self, bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command(name='addcommand',
                      help="!addcommand <command_name> <response>",
                      description="Adds a custom command with a response.")
    @commands.has_permissions(administrator=True)
    async def add_command(self, ctx,
        command_name: str = commands.parameter(description=DESCR_CMD_NAME),*,
        response: str = commands.parameter(description=DESCR_CMD_RESPONSE)):
        try:
            if not command_name or not response:
                await ctx.send("Befehlsname und Antwort dürfen nicht leer sein.")
                raise ValueError("Befehlsname und Antwort dürfen nicht leer sein.")
            if self.storage.exists(command_name):
                await ctx.send(f"Befehl '{command_name}' existiert bereits. "
                                 f"Bitte wähle einen anderen Namen.")
                return
            self.storage.set(command_name, response)
            await ctx.send(f"Befehl '{command_name}' wurde erfolgreich hinzugefügt.")
        except ValueError as e:
            await ctx.send(str(e))

    @commands.command(name='removecommand',
                      description="Removes a custom command.",
                      help="!removecommand <command_name>")
    @commands.has_permissions(administrator=True)
    async def remove_command(self, ctx,
        command_name: str = commands.parameter(description=DESCR_CMD_NAME)):
        try:
            if not self.storage.exists(command_name):
                await ctx.send(f"Befehl '{command_name}' existiert nicht. "
                                 f"Bitte überprüfe den Befehl und versuche es erneut.")
                return
            self.storage.delete(command_name)
            await ctx.send(f"Befehl '{command_name}' wurde erfolgreich entfernt.")
        except ValueError as e:
            await ctx.send(str(e))

    @commands.command(name='customcommand',
                      description="Executes a custom command.",
                      help="!customcommand <command_name>")
    async def custom_command(self, ctx,
        command_name: str = commands.parameter(description=DESCR_CMD_NAME)):
        try:
            if not command_name:
                await ctx.send("Gib einen Befehlnamen ein SOFORT!!!")
                raise ValueError("Befehlsname darf nicht leer sein.")
            if not self.storage.exists(command_name):
                await ctx.send(f"Es gibt keinen Befehl mit dem Namen: '{command_name}'. "
                                 f"Bitte überprüfe den Befehl und versuche es erneut "
                                 f"ODER erstelle einen Befehl mit diesem Namen.")
                return
            await ctx.send(self.storage.get(command_name))
        except ValueError as e:
            ctx.send(str(e))
            return




