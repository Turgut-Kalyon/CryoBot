


class DailyCoinsMessenger:

    def __init__(self, channel):
        self.channel = channel

    async def send_already_claimed_message(self):
        await self.channel.send("Du hast deine täglichen Coins bereits abgeholt. Du kannst sie jeden Tag um 00:00 Uhr abholen.")


    async def send_reward_claimed_message(self):
        await self.channel.send(f"{self.channel.author.mention} hat {self.daily_coins} coins bekommen.")
