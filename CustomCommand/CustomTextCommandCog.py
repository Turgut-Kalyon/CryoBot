from discord.ext import commands
from CustomCommand.CustomCommandStorage import CustomCommandStorage

DESCR_CMD_NAME = "Name of the command"
DESCR_CMD_RESPONSE = "Response to the command"


class CustomTextCommandCog(commands.Cog, description="Custom text command handler for CryoBot"):

    @property
    def qualified_name(self):
        return "Custom Commands"

    def __init__(self, bot):
        self.bot = bot
        self.command_handler = CustomCommandStorage()

    @commands.command(name='addcommand',
                      help="!addcommand <command_name> <response>",
                      description="Adds a custom command with a response.")
    @commands.has_permissions(administrator=True)
    async def add_command(self, ctx,
        command_name: str = commands.parameter(description=DESCR_CMD_NAME),*,
        response: str = commands.parameter(description=DESCR_CMD_RESPONSE)):
        try:
            self.command_handler.add_command(command_name, response)
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
            self.command_handler.remove_command(command_name)
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
                raise ValueError("Gib einen Befehlnamen ein SOFORT!!!")
            response = self.command_handler.get_command_response(command_name)
            if response is None:
                raise ValueError(f"Es gibt keinen Befehl mit dem Namen: '{command_name}'. "
                                 f"Bitte überprüfe den Befehl und versuche es erneut "
                                 f"ODER erstelle einen Befehl mit diesem Namen.")
            await ctx.send(response)
        except ValueError as e:
            ctx.send(str(e))
            return




