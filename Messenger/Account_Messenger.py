


class AccountMessenger:

    async def send_account_created_message(self, ctx, user):
        await ctx.send(f"{user.mention}, Dein Konto wurde erfolgreich erstellt!")

    async def send_balance_message(self, ctx, user, balance):
        await ctx.send(f"{user.mention}, Du besitzt aktuell {balance} coins.")

    async def send_already_has_account_message(self, ctx, user):
        await ctx.send(f"{user.mention}, Du hast bereits ein Konto.")

    async def send_no_account_message(self, ctx):
        await ctx.send(f"{ctx.author.mention}, Du hast kein Konto.")

    async def send_can_not_afford_message(self, ctx, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, du hast nicht genug Coins, um das Spiel zu starten. "
                       f"Du benötigst mindestens {minimum_bet} coins.")
