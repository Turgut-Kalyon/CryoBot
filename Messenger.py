


# TODO: add bet validatior for Messenger
class Messenger:


    async def send_bet_is_too_low(self, ctx, minimum_bet):
        await ctx.send(f"Der Einsatz muss mindestens {minimum_bet} coins betragen.")

    async def send_bet_is_too_high(self, ctx, maximum_bet):
        await ctx.send(f"Der Einsatz darf nicht höher als {maximum_bet} sein.")

    async def send_it_has_to_be_positive_number(self, ctx):
        await ctx.send("Der Einsatz muss eine positive Zahl sein.")

    async def send_player_wants_to_quit_the_game(self, ctx):
        await ctx.send("Spiel abgebrochen.")

    async def send_bet_request_accepted(self, bet, ctx):
        await ctx.send(f"Dein Einsatz von {bet.content} coins wurde akzeptiert. Viel Glück!")

    async def send_bet_request_message(self, ctx, maximum_bet, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, bitte gib deinen Einsatz"
                       f"(minimum={minimum_bet} und maximum={maximum_bet}) an, um das Spiel zu starten.")
        
    async def send_no_account_message(self, ctx):
        await ctx.send(
            f"{ctx.author.mention}, du hast kein Konto. Erstelle ein Konto mit !cracc, um das Spiel zu starten.")

    async def send_can_not_afford_message(self, ctx, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, du hast nicht genug Coins, um das Spiel zu starten. "
                       f"Du benötigst mindestens {minimum_bet} coins."
                       f"\n\ndein aktueller Kontostand: {self.coin_storage.get(ctx.author.id)}")
        

    async def send_bet_validation_error(self, ctx):
        if await self.bet_validator.is_bet_negative(self.current_bet):
            await self.send_it_has_to_be_positive_number(ctx)
        elif await self.bet_validator.is_bet_too_high(self.current_bet):
            await self.send_bet_is_too_high(ctx)
        elif await self.bet_validator.is_bet_too_low(self.current_bet):
            await self.send_bet_is_too_low(ctx)
        else:
            await ctx.send("Ungültiger Einsatz.")
