from datetime import datetime, time
from discord.ext import commands, tasks
from CurrencySystem.CoinTransfer import CoinTransfer
from Storage import Storage

class DailyCoins(commands.Cog):
    def __init__(self, bot, storage: Storage, coin_transfer: CoinTransfer):
        self.bot = bot
        self.daily_coins = 10
        self.storage = storage
        self.coin_transfer = coin_transfer

    def cog_unload(self):# pragma: no cover
        self.clear_yaml_task.cancel()

    @tasks.loop(minutes=1)
    async def clear_yaml_task(self):
        now = datetime.now().time()
        if self.is_new_day(now):
            self.storage.set_all(None)

    @staticmethod
    def is_new_day(now):
        return time(0, 0) <= now < time(0, 1)

    def add_daily_reward_to_user(self, ctx):
        self.coin_transfer.add_coins(ctx.author.id, self.daily_coins)
        self.mark_daily_rewards_as_claimed(ctx)

    def mark_daily_rewards_as_claimed(self, ctx):
        current_time = datetime.now().time().strftime("%H:%M:%S")
        self.storage.set(ctx.author.id, current_time)

    async def send_no_account_message(self, ctx):
        await ctx.send(f"{ctx.author.mention}, Du hast noch kein Konto. Erstelle ein Konto mit !cracc, um tägliche Coins zu erhalten.")

    async def send_already_claimed_message(self, ctx):
        await ctx.send("Du hast deine täglichen Coins bereits abgeholt. Du kannst sie jeden Tag um 00:00 Uhr abholen.")

    async def send_reward_claimed_message(self, ctx):
        await ctx.send(f"{ctx.author.mention} hat {self.daily_coins} coins bekommen.")


    @commands.command(name='daily', help="!daily", description="Claim your daily coins.")
    async def claim_daily_reward(self, ctx):
        if not self.has_account(ctx):
            await self.send_no_account_message(ctx)
            return
        if self.has_user_received_daily_reward(ctx):
            await self.send_already_claimed_message(ctx)
            return
        self.add_daily_reward_to_user(ctx)
        await self.send_reward_claimed_message(ctx)

    @property
    def qualified_name(self):# pragma: no cover
        return "Currency System"


