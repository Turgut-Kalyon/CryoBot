from datetime import datetime, time
from discord.ext import commands, tasks
from FileOperations import CoinsFileOperations
from CurrencySystem.CoinTransfer import CoinTransfer

file_path = '/files/daily.yaml'

class DailyCoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_coins = 10
        self.coin_transfer = CoinTransfer()
        self.file_operator = CoinsFileOperations(file_path)
        self.user_daily_file = self.file_operator.load_file().get('users')

    def cog_unload(self):
        self.clear_yaml_task.cancel()

    @tasks.loop(minutes=1)
    async def clear_yaml_task(self):
        now = datetime.now().time()
        if self.is_new_day(now):
            self.file_operator.clear_yaml()

    @staticmethod
    def is_new_day(now):
        return time(0, 0) <= now < time(0, 1)

    @commands.command(name='daily', help="!daily", description="Claim your daily coins.")
    async def daily(self, ctx):
        if not self.user_daily_file:
            await self.add_daily_reward_to_user(ctx)
            return
        if ctx.author.id in self.user_daily_file:
            await ctx.send("Du hast deine täglichen Coins bereits abgeholt. "
                                "Du kannst sie jeden Tag um 00:00 Uhr abholen.")
            return
        await self.add_daily_reward_to_user(ctx)

    def has_claimed_daily_reward(self, ctx):
        return ctx.author.id in self.user_daily_file

    async def add_daily_reward_to_user(self, ctx):
        self.coin_transfer.add_coins(ctx.author.id, self.daily_coins)
        self.user_daily_file[ctx.author.id] = datetime.now().isoformat()
        self.file_operator.write_file(self.user_daily_file)
        await ctx.send(f"{ctx.author.mention} hat {self.daily_coins} coins bekommen.")

    @property
    def qualified_name(self):
        return "Currency System"


