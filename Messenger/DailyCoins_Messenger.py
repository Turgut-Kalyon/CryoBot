


class DailyCoinsMessenger:


    async def send_already_claimed_message(self, ctx):
        await ctx.send("Du hast deine täglichen Coins bereits abgeholt. Du kannst sie jeden Tag um 00:00 Uhr abholen.")


    async def send_reward_claimed_message(self, ctx):
        await ctx.send(f"{ctx.author.mention} hat {self.daily_coins} coins bekommen.")
