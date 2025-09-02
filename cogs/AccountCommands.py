"""
Author: Turgut Kalyon
Description: Account module for CryoBot, providing functionalities related to user accounts.
It's managing the coins of users, allowing them to check their balance, and providing a way to add coins.
"""
from discord.ext import commands
import random
from account.Account import Account
from account.AccountService import AccountService
from account.AccountValidator import AccountValidator


class AccountCommands(commands.Cog):
    def __init__(self, bot, account_service : AccountService):
        self.bot = bot
        self.account_service = account_service
        self.account_validator = AccountValidator(self.account_service.get_all_accounts())
        self.quotes = [
            "Keep your coins close, but your friends closer.",
            "Coins are like friends, the more you have, the better.",
            "A coin saved is a coin earned.",
            "Invest in yourself, it's the best return on investment.",
            "Coins may come and go, but memories last forever."
        ]

    @commands.command(name='balance', help="!balance", description="Check your coin balance.")
    async def send_balance(self, ctx):
        user_id = ctx.author.id
        balance = self.account_service.get_account(user_id).balance
        await ctx.send(f"{ctx.author.mention}, Du besitzt aktuell {balance} coins.")

    @staticmethod
    def has_bot_written_the_message(ctx):# pragma: no cover
        return ctx.author.bot

    @commands.command(name='cracc', help="!cracc", description="create an account for daily rewards and fun games.")
    async def create_account(self, ctx):
        user_id = ctx.author.id
        if self.account_validator.has_account(user_id):
            await ctx.send(f"{ctx.author.mention}, Du hast bereits ein Konto.")
            return
        await self.init_account(ctx, user_id)

    async def init_account(self, ctx, user_id):
        account = Account(user_id)
        self.account_service.create_account(user_id)
        await ctx.send(f"{ctx.author.mention}, Dein Konto wurde erfolgreich erstellt!")

    @property
    def qualified_name(self):# pragma: no cover
        return "Account Commands"






