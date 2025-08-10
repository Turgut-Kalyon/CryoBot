# CryoBot

<img src="https://socialify.git.ci/Turgut-Kalyon/CryoBot/image?font=JetBrains+Mono&language=1&name=1&owner=1&pattern=Solid&theme=Dark" alt="CryoBot" width="640" height="320" />

CryoBot is a Discord bot designed to enhance server interactions by allowing users to create and manage custom text commands. Built with Python and `discord.py`, it provides a modular architecture for easy command management and extensibility.

## Features

-   **Modular Design:** Utilizes `discord.py` Cogs for organized and scalable command management.
-   **Custom Text Command:** Allows users to create custom text-based commands on-the-fly.

## Commands

The bot responds to the following commands. The default prefix is `!`.

-   `!help <command_name>`
    -   Displays a list of all available commands.
    -   When a specific command is provided (e.g., `!help addcommand`), it shows detailed information, including description and usage for that command.

-   `!hello`
    -   A simple command that makes the bot greet the user who sent the message.

-   `!addcommand <command_name> <response>`
    -   Creates a custom text-based command.

-   `!removecommand <command_name>`
    -   Removes a custom text-based command.

-   `!customcommand <command_name>`
    -   Executes a created custom text-based command.

-   `!listcommands`
    -   Lists all custom text-based commands that have been created.



## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   Python 3.8+
-   A Discord Bot Token. You can create one on the [Discord Developer Portal](https://discord.com/developers/applications).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/turgut-kalyon/cryobot.git
    cd cryobot
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment. The bot relies on the following libraries:
    -   `discord.py`
    -   `PyYAML`
    -   `python-dotenv`

    You can install them using pip:
    ```sh
    pip install discord.py pyyaml python-dotenv
    ```

3.  **Configure the environment:**
    -   Create a file named `.env` in the root directory of the project.
    -   Add your Discord bot token to this file:
    ```
    TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
    ```

### Running the Bot

Execute the main script to start the bot:
```sh
python main.py
```
You should see a confirmation message in your console once the bot has successfully logged in.

If you have a raspberry pi, you can run the bot with the following command. I would recommend using a terminal multiplexer like `tmux` or `screen` to keep the bot running in the background.:
```sh
screen -S cryobot
cd /cryobot
source venv/bin/activate  # Activate your virtual environment if you are using one
python3 main.py
```

## Project Structure

```
.
├── CryoBot.py                      # Defines the main CryoBot class and core event handlers.
├── FileOperations.py               # Utility class for reading and writing YAML files.
├── CustomCommands/
    ├── CustomCommandStorage.py     # Handles storage and retrieval of custom commands.
    └── CustomTextCommandCog.py     # Manages custom text commands.
├── main.py                         # The main entry point for the application.
└── response/
    └── custom_commands.yaml        # YAML file containing command name and response for the custom text commands.