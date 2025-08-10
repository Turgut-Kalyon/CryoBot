import asyncio
import os
from dotenv import load_dotenv
from CryoBot import CryoBot
from HelpCog import HelpCog

load_dotenv()
cryo_bot = CryoBot()

async def setup_cogs():
    await cryo_bot.add_cog(HelpCog(cryo_bot))
    print("Cogs have been loaded successfully.")

async def setup():
    await setup_cogs()
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("TOKEN environment variable not set or empty")
    print("Starting CryoBot...")
    await cryo_bot.start(token)

if __name__ == "__main__":
    asyncio.run(setup())