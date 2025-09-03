


class AccountMessenger:
    def __init__(self, channel):
        self.channel = channel

    async def send_account_created_message(self, user):
        await self.channel.send(f"{user.mention}, Dein Konto wurde erfolgreich erstellt!")

    async def send_balance_message(self, user, balance):
        await self.channel.send(f"{user.mention}, Du besitzt aktuell {balance} coins.")

    async def send_already_has_account_message(self, user):
        await self.channel.send(f"{user.mention}, Du hast bereits ein Konto.")

    async def send_no_account_message(self, user):
        await self.channel.send(f"{user.mention}, Du hast kein Konto.")

   