


# TODO: add bet validatior for Messenger
class Messenger:






    async def send_player_wants_to_quit_the_game(self, ctx):
        await ctx.send("Spiel abgebrochen.")

    async def send_bet_request_accepted(self, bet, ctx):
        await ctx.send(f"Dein Einsatz von {bet.content} coins wurde akzeptiert. Viel Glück!")

    async def send_bet_request_message(self, ctx, maximum_bet, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, bitte gib deinen Einsatz"
                       f"(minimum={minimum_bet} und maximum={maximum_bet}) an, um das Spiel zu starten.")
        
    async def send_can_not_afford_message(self, ctx, minimum_bet):
        await ctx.send(f"{ctx.author.mention}, du hast nicht genug Coins, um das Spiel zu starten. "
                       f"Du benötigst mindestens {minimum_bet} coins."
                       f"\n\ndein aktueller Kontostand: {self.coin_storage.get(ctx.author.id)}")
        

