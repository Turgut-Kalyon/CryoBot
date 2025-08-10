"""
Author: Turgut Kalyon
Description: Main entry point for the CryoBot application.
This script initializes the CryoBot, loads environment variables, and sets up cogs.
"""
import asyncio
import os
from dotenv import load_dotenv
from CryoBot import CryoBot
from CustomCommand.CustomTextCommandCog import CustomTextCommandCog

load_dotenv()
cryo_bot = CryoBot()

def get_token():
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("TOKEN environment variable not set or empty")
    return token

async def setup_cogs():
    await cryo_bot.add_cog(CustomTextCommandCog(cryo_bot))
    print("Cogs have been loaded successfully.")

async def setup():
    await setup_cogs()
    token = get_token()
    print("Starting CryoBot...")
    await cryo_bot.start(token)

if __name__ == "__main__":
    asyncio.run(setup())