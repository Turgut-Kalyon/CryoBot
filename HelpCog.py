"""
Author: Turgut Kalyon
Description: HelpCog for CryoBot, providing help information for commands.
"""
from FileOperations import FileOperations
from discord.ext import commands

class HelpCog(commands.Cog, description="Provides help information for commands"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.loaded_commands = FileOperations('/response/help.yaml').load_file()['commands']
        self.response = None


    @commands.command(name='cryohelp',
                      help="Provides help information for commands", )
    async def cryohelp(self ,ctx, passed_command_name=None):
        self.response = None
        if not self.is_command_name_given(passed_command_name):
            await self.send_help_page_overview(ctx)
            return
        specific_command = self.loaded_commands.get(passed_command_name, None)
        if not self.does_command_exist(specific_command):
            await ctx.send(f"No help information found for command: {passed_command_name}")
            return
        await self.send_specific_help_page(specific_command, passed_command_name, ctx)
        self.bot.process_commands(ctx.message)

    @staticmethod
    def is_command_name_given(command_name):
        return command_name is not None

    @staticmethod
    def does_command_exist(command_name):
        return command_name

    def     send_help_page_overview(self, ctx):
        self.response = "Available commands:\n"
        for page in self.loaded_commands:
            print(page['name'])
            self.generate_specific_help_page(page, page['name'])
            self.response += '\n\n'
        return ctx.send(self.response)

    def send_specific_help_page(self, specific_command, command_name, ctx):
        self.response = ""
        self.generate_specific_help_page(specific_command, command_name)
        return ctx.send(self.response)

    def generate_specific_help_page(self, specific_command, command_name):
        self.append_description(specific_command, command_name)
        self.append_usage(specific_command)
        self.append_examples(specific_command)
        self.append_options(specific_command)

    def append_description(self, specific_command, command_name):
        self.response += f"**{command_name}**: {specific_command['description']}\n"

    def append_usage(self, specific_command):
        if 'usage' in specific_command:
            self.response += f"**Usage**: {specific_command['usage']}\n"

    def append_examples(self, specific_command):
        if 'examples' in specific_command:
            self.response += "**Examples**:\n"
            for example in specific_command['examples']:
                self.response += f"- {example}\n"


    def append_options(self, specific_command):
        if 'options' in specific_command:
            self.response += "**Options**:\n"
            for option in specific_command['options']:
                self.response += f"- **{option['name']}**: {option['description']}\n"


