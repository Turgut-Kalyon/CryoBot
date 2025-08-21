# CryoBot

CryoBot is a versatile Discord bot built with Python and the `discord.py` library. It enhances server engagement through a customizable command system, a user economy, and daily rewards. Its modular architecture, based on Cogs, allows for easy expansion and maintenance.

## Features

-   **Custom Commands**: Server administrators can dynamically add, remove, and execute simple text-based commands.
-   **Economy System**: Users can create an account, check their balance, and earn daily coins.
-   **Games**: Bet coins in fun games — the winner gets paid! 
-   **Persistent Storage**: User data, custom commands, and daily reward statuses are saved in YAML files, ensuring data persistence across bot restarts.
-   **Modular Design**: Commands are organized into Cogs (`AccountCommands`, `CustomTextCommandCog`, `DailyCoins`) for clean and scalable code.
-   **Robust Testing**: Includes a comprehensive suite of unit and integration tests using `pytest`, integrated into a Jenkins CI/CD pipeline.
-   **Error Handling**: A dedicated error handler cog provides feedback for failed commands.

## Commands

The default command prefix is `!`.

| Command | Description | Usage | Permissions |
| :--- | :--- | :--- | :--- |
| `!hello` | Greets the user with a random quote. | `!hello` | Everyone |
| `!cracc` | Creates a new user account with starting coins. | `!cracc` | Everyone |
| `!balance` | Checks your current coin balance. | `!balance` | Everyone |
| `!daily` | Claims your daily coin reward. Can be used once per day. | `!daily` | Everyone |
| `!addcommand` | Adds a new custom text command. | `!addcommand <name> <response>` | Administrator |
| `!removecommand`| Removes an existing custom command. | `!removecommand <name>` | Administrator |
| `!execCommand` | Executes a custom command and shows its response. | `!execCommand <name>` | Everyone |
| `!guess` | Starts the guessing game. | `!guess` | Everyone |

## Getting Started

Follow these instructions to get a local copy of CryoBot up and running.

### Prerequisites

-   Python 3.8+
-   A Discord Bot Token. You can create one on the [Discord Developer Portal](https://discord.com/developers/applications).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Turgut-Kalyon/CryoBot.git
    cd CryoBot
    ```

2.  **Set up a virtual environment:**
    ```sh
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies from `requirements.txt`:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure the environment:**
    -   Create a file named `.env` in the root directory of the project.
    -   Add your Discord bot token to this file. The `main.py` script will load this variable.
    ```env
    TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
    ```

### Running the Bot

Execute the `main.py` script to start the bot:
```sh
python main.py
```
You should see a confirmation message in your console once the bot has successfully logged in and loaded its cogs.

## Project Structure

The repository is organized to separate concerns, making it easier to navigate and maintain.

```
CryoBot/
├── main.py                    # Main entry point, loads cogs and starts the bot.
├── CryoBot.py                 # Defines the core bot class, subclass of discord.ext.commands.Bot.
├── Storage.py                 # Handles reading from and writing to YAML data files.
├── ErrorHandler.py            # Cog for handling command errors globally.
├── requirements.txt           # Lists all Python dependencies for the project.
│
├── cogs/                      # Contains all command modules (Cogs).
│   ├── AccountCommands.py     # Manages user accounts, balance, and greetings.
│   ├── CustomTextCommandCog.py# Manages creation, deletion, and execution of custom commands.
│   └── DailyCoins.py          # Handles the daily coin reward system.
│
├── CurrencySystem/            # Contains the logic for the economy features.
│   └── CoinTransfer.py        # Implements coin transactions (add/remove).
│
├── files/                     # Stores persistent data in YAML format.
│   ├── coins.yaml             # Stores user coin balances.
│   ├── commands.yaml          # Stores custom command definitions.
│   └── daily.yaml             # Stores timestamps for daily reward claims.
│
└── tests/                     # Contains all tests for the application.
    ├── unittests/             # Unit tests for individual components.
    ├── Integrationtests/      # Integration tests for combined components.
    └── jenkins/               # Jenkins CI/CD pipeline configuration (groovy scripts).
```

## Testing

The project is configured for continuous integration with Jenkins. The `tests/jenkins/jenkinsfile.groovy` defines a pipeline that prepares a virtual environment, installs dependencies, and runs a full suite of unit (`tests/unittests`) and integration tests (`tests/Integrationtests`) using `pytest`. Test results are generated in JUnit XML format for reporting.
