# CryoBot

CryoBot is a versatile and modular Discord bot built with `discord.py`. It is designed for easy extension, featuring a dynamic help command system that reads its data directly from a YAML configuration file.

## Features

-   **Modular Design:** Utilizes `discord.py` Cogs for organized and scalable command management.
-   **Dynamic Help Command:** The `!cryhelp` command's content is loaded from `/response/help.yaml`, allowing for easy updates to command descriptions, usage, and examples without modifying the bot's code.
-   **Environment-based Configuration:** Securely manages the bot's token using a `.env` file.
-   **Simple Event Handling:** Includes basic event listeners for `on_ready` and `on_message` events.

## Commands

The bot responds to the following commands. The default prefix is `!`.

-   `!cryhelp [command]`
    -   Displays a list of all available commands.
    -   When a specific command is provided (e.g., `!cryhelp hello`), it shows detailed information, including description, usage, and examples for that command.

-   `!hello`
    -   A simple command that makes the bot greet the user who sent the message.

-   `!createtxtcmd <command> <response>`
    -   Creates a custom text-based command.

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   Python 3.8+
-   A Discord Bot Token. You can create one on the [Discord Developer Portal](https://discord.com/developers/applications).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/turgut-kalyon/discordbot.git
    cd discordbot
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

## Project Structure

```
.
├── CryoBot.py        # Defines the main CryoBot class and core event handlers.
├── FileOperations.py # Utility class for reading and writing YAML files.
├── HelpCog.py        # Implements the dynamic !cryhelp command logic.
├── main.py           # The main entry point for the application.
└── response/
    └── help.yaml     # Configuration file for the help command's content.