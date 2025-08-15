"""
Author: Turgut Kalyon
Description: Account module for CryoBot, providing functionalities related to user accounts.
It's managing the coins of users, allowing them to check their balance, and providing a way to add coins.
"""
from discord.ext import commands
import random
from CurrencySystem.CoinTransfer import CoinTransfer
from Storage import Storage


class AccountCommands(commands.Cog):
    def __init__(self, bot, coin_transfer: CoinTransfer, coin_storage: Storage, daily_storage: Storage):
        self.bot = bot
        self.coin_transfer = coin_transfer
        self.coin_storage = coin_storage
        self.daily_storage = daily_storage

        self.quotes = [
            "Keep your coins close, but your friends closer.",
            "Coins are like friends, the more you have, the better.",
            "A coin saved is a coin earned.",
            "Invest in yourself, it's the best return on investment.",
            "Coins may come and go, but memories last forever."
        ]

    @commands.command(name='balance', help="!balance", description="Check your coin balance.")
    async def balance(self, ctx):
        user_id = ctx.author.id
        balance = self.coin_storage.get(user_id)
        if balance is None:
            await ctx.send(f"{ctx.author.mention}, Du hast noch kein Konto. "
                           "Erstelle ein Konto mit !cracc, um dein Guthaben zu überprüfen.")
            return
        await ctx.send(f"{ctx.author.mention}, Du besitzt aktuell {balance} coins.")

    @commands.command(name='hello', help="!hello", description="Sends a greeting message.")
    async def hello(self, ctx):
        if ctx.author.bot:
            return
        await ctx.send(f'Hallo {ctx.author.mention}!\n'
                       f'Hier ist dein persönliches Zitat:\n'
                       f'*"{self.get_random_quote()}"*')

    @commands.command(name='cracc', help="!cracc", description="create an account for daily rewards and fun games.")
    async def cracc(self, ctx):
        user_id = ctx.author.id
        if self.coin_storage.exists(user_id):
            await ctx.send(f"{ctx.author.mention}, Du hast bereits ein Konto.")
        else:
            await self.init_account(user_id)
            await ctx.send(f"{ctx.author.mention}, Dein Konto wurde erfolgreich erstellt!")

    async def init_account(self, user_id):
        starting_coins = self.coin_transfer.get_starting_coins()
        self.coin_storage.set(user_id, starting_coins)
        self.daily_storage.set(user_id, None)

    def get_random_quote(self):
        return random.choice(self.quotes)

    @property
    def qualified_name(self):
        return "Account Commands"






