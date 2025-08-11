from FileOperations import CustomCommandsFileOperations


class CustomCommandStorage:

    def __init__(self):
        self.storage = CustomCommandsFileOperations('/response/commands.yaml')
        self.custom_commands = self.storage.load_file().get('commands', {})

    def add_command(self, command_name, response):
        if command_name in self.custom_commands:
            raise ValueError(f"Command '{command_name}' already exists.")
        self.custom_commands[command_name] = response
        self.storage.write_file(self.custom_commands)

    def remove_command(self, command_name):
        if command_name not in self.custom_commands:
            raise ValueError(f"Command '{command_name}' does not exist.")
        del self.custom_commands[command_name]
        self.storage.write_file(self.custom_commands)

    def get_command_response(self, command_name):
        return self.custom_commands.get(command_name, None)
