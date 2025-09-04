"""
Author: Turgut Kalyon
Description: Main entry point for the CryoBot application.
This script initializes the CryoBot, loads environment variables, and sets up cogs.
"""
import asyncio
import os
from dotenv import load_dotenv
from account.AccountRepository import AccountRepository
from account.AccountService import AccountService
from cogs.AccountCommands import AccountCommands
from CryoBot import CryoBot
from CurrencySystem.CoinTransfer import CoinTransfer
from cogs.DailyCoins import DailyCoins
from cogs.CustomTextCommandCog import CustomTextCommandCog
from ErrorHandler import ErrorHandler
from Storage import Storage
from cogs.Games.GuessingGame import GuessingGame

load_dotenv()# pragma: no cover
cryo_bot = CryoBot()# pragma: no cover


def get_token():# pragma: no cover
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("TOKEN environment variable not set or empty")
    return token


async def setup_cogs():# pragma: no cover
    current_directory = os.getcwd()
    storage = Storage(os.path.join(current_directory, 'account_data.yaml'), 'accounts')
    coin_transfer = CoinTransfer(storage)
    account_repository = AccountRepository(storage)
    account_service = AccountService(account_repository)



    #await cryo_bot.add_cog(CustomTextCommandCog(cryo_bot, storage_commands))
    await cryo_bot.add_cog(AccountCommands(cryo_bot, account_service))
    await cryo_bot.add_cog(DailyCoins(cryo_bot, account_service))
    await cryo_bot.add_cog(ErrorHandler(cryo_bot))
    await cryo_bot.add_cog(GuessingGame(cryo_bot, account_service))
    print("Cogs have been loaded successfully.")


async def setup():# pragma: no cover
    await setup_cogs()
    token = get_token()
    print("Starting CryoBot...")
    await cryo_bot.start(token)


if __name__ == "__main__":
    asyncio.run(setup())
