from menu import Menu, Option

def busy_withdraw(world): world.business.withdraw(world)
def busy_inspect(world): world.business.inspect()
def busy_purchase(world): world.business.purchase(world)
def busy_sell(world): world.business.sell(world)

menu_business = Menu(
    "Manage Business", "How can we help you", [
        Option("Withdraw earnings", '', 'w', busy_withdraw),
        Option("Inspect Businesses", '', 'i', busy_inspect),
        Option("Purchase new Business", '', 'p', busy_purchase),
        Option("Sell Businesses", '', 's', busy_sell)
    ]
)
