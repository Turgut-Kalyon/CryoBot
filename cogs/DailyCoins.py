from datetime import datetime, time
from discord.ext import commands, tasks
from CurrencySystem.CoinTransfer import CoinTransfer
from Storage import Storage
from account import AccountValidator
from account.AccountService import AccountService

class DailyCoins(commands.Cog):
    def __init__(self, bot, account_service: AccountService):
        self.bot = bot
        self.daily_coins = 10
        self.account_service = account_service
        self.account_validator = AccountValidator(self.account_service.get_all_accounts())

    def cog_unload(self):# pragma: no cover
        self.clear_yaml_task.cancel()

    @tasks.loop(minutes=1)
    async def clear_yaml_task(self):
        now = datetime.now().time()
        if self.is_new_day(now):
            self.account_service.reset_daily_claims()

    @staticmethod
    def is_new_day(now):
        return time(0, 0) <= now < time(0, 1)

    
    @commands.command(name='daily', help="!daily", description="Claim your daily coins.")
    async def claim_daily_reward(self, ctx):
        account = self.account_service.get_account(ctx.author.id)
        if self.account_validator.has_received_daily_reward(account):
            await self.send_already_claimed_message(ctx)
            return
        self.account_service.add_daily_reward_to_user(account)
        await self.send_reward_claimed_message(ctx)


    async def send_already_claimed_message(self, ctx):
        await ctx.send("Du hast deine täglichen Coins bereits abgeholt. Du kannst sie jeden Tag um 00:00 Uhr abholen.")


    async def send_reward_claimed_message(self, ctx):
        await ctx.send(f"{ctx.author.mention} hat {self.daily_coins} coins bekommen.")


    @property
    def qualified_name(self):# pragma: no cover
        return "Currency System"


