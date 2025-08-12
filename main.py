"""
Author: Turgut Kalyon
Description: Main entry point for the CryoBot application.
This script initializes the CryoBot, loads environment variables, and sets up cogs.
"""
import asyncio
import os
from dotenv import load_dotenv
from AccountCommands import AccountCommands
from CryoBot import CryoBot
from CurrencySystem.DailyCoins import DailyCoins
from CustomCommand.CustomTextCommandCog import CustomTextCommandCog
from ErrorHandler import ErrorHandler

load_dotenv()
cryo_bot = CryoBot()


def get_token():
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("TOKEN environment variable not set or empty")
    return token


async def setup_cogs():
    await cryo_bot.add_cog(CustomTextCommandCog(cryo_bot))
    await cryo_bot.add_cog(AccountCommands(cryo_bot))
    await cryo_bot.add_cog(DailyCoins(cryo_bot))
    await cryo_bot.add_cog(ErrorHandler(cryo_bot))
    print("Cogs have been loaded successfully.")


async def setup():
    await setup_cogs()
    token = get_token()
    print("Starting CryoBot...")
    await cryo_bot.start(token)


if __name__ == "__main__":
    asyncio.run(setup())
