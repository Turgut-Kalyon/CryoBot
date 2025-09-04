from datetime import datetime, time
from discord.ext import commands, tasks
from Messenger.DailyCoins_Messenger import DailyCoinsMessenger
from account import AccountValidator
from account.AccountService import AccountService

class DailyCoins(commands.Cog):
    def __init__(self, bot, account_service: AccountService):
        self.bot = bot
        self.daily_coins = 10
        self.account_service = account_service
        self.account_validator = AccountValidator(self.account_service.get_all_accounts())
        self.daily_coins_messenger = DailyCoinsMessenger()

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
            await self.daily_coins_messenger.send_already_claimed_message()
            return
        self.account_service.add_daily_reward_to_user(account)
        await self.daily_coins_messenger.send_reward_claimed_message()


    @property
    def qualified_name(self):# pragma: no cover
        return "Currency System"


