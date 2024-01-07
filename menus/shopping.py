from math import floor
from os import system

from menu import Menu, Option, input_buffer, valid_numeric_input, coming_soon

from resources.strings import casino_phrase

def shop_purchase_qty(world, cost):
    money = world.player.money
    if money < cost: return None

    max_purchase = floor(money / cost)
    default = min(len(world.player.crew), max_purchase)

    return valid_numeric_input(
        "How many would you like to purchase (0 to cancel)", 0, max_purchase, default
    )

def purchase(world, cost, qty):
    if qty == None:
        print("\nYou do not have enough money for that")
        input_buffer()
        return 0

    cost = cost * qty
    world.player.money -= cost
    return qty


def shop_buy_armor(world):
    qty = purchase(world, 100, shop_purchase_qty(world, 100))
    world.player.vests += qty

shop_weapons = ["bat", "pistol", "shotgun", "rifle"]

def shop_buy_weapon(world, index):
    wep = world.weapons.lookup_weapon(shop_weapons[index])
    qty = purchase(world, wep.price, shop_purchase_qty(world, wep.price))
    world.player.give_weapon(wep.id, qty)

def shop_buy_bat(world): shop_buy_weapon(world, 0)
def shop_buy_pistol(world): shop_buy_weapon(world, 1)
def shop_buy_shotgun(world): shop_buy_weapon(world, 2)
def shop_buy_rifle(world): shop_buy_weapon(world, 3)

# Need function instead of menu to handle printing prices
menu_buy_gear = Menu(
    "Purchase Gear", "What would you like to buy", [
        Option("$20 Baseball Bat", '', 'b', shop_buy_bat),
        Option("$100 Armor", '', 'a', shop_buy_armor),
        Option("$200 Pistol", '', 'p', shop_buy_pistol),
        Option("$400 Shotgun", '', 's', shop_buy_shotgun),
        Option("$600 Rifle", '', 'r', shop_buy_rifle)
    ]
)


def bank_deposit(world): world.bank.deposit_savings(world)
def bank_withdraw(world): world.bank.withdraw_savings(world)
def bank_take_loan(world): world.bank.take_loan(world)
def bank_pay_loan(world): world.bank.pay_loan(world)


menu_bank = Menu(
    "The Bank", "How can we help you sir", [
        Option("Deposit Money", '', 'd', bank_deposit),
        Option("Withdraw Money", '', 'w', bank_withdraw),
        Option("Request Loan", '', 'l', bank_take_loan),
        Option("Make Loan Payment", '', 'p', bank_pay_loan)
    ]
)


def shady_donation(world):
    ply = world.player
    print("Money: $", ply.money, sep='')

    donation = valid_numeric_input(
        "How much money are we forking over", 0, ply.money, (ply.money // 2)
    )

    if donation > 0:
        ply.money -= donation
        heat_change = (donation // (ply.heat_cap // 10))
        ply.heat_cap += heat_change

        print('$', donation, " donated to the feds", sep='')
        input_buffer()

def hire_lawyers(world):
    ply = world.player
    lawyers = world.lawyers
    count = lawyers.count
    cost = lawyers.cost
    can_afford = min(ply.money // cost, lawyers.max_count - count)

    if can_afford == 0:
        if count == lawyers.max_count:
            print("We've already hired every Lawyer in the country!")
        else:
            print(
                "You can't afford any Lawyers, They're $", cost, " a pop!", 
            sep='')

        input_buffer()
        return

    print("Cost per Lawyer: $", cost, " every ", lawyers.turns, " turns", sep='')
    print("\nLawyers on the books:", lawyers.count)
    print("Current cost every", lawyers.turns, "turns: $", (cost * count), sep='')

    print("\nMoney: $", ply.money, sep='')

    hiring = valid_numeric_input(
        "\nHow many Lawyers are we hiring", 0, can_afford, 0
    )

    if hiring == 0: return

    lawyers.count += hiring
    cost *= hiring
    ply.money -= cost

    print("\nHired ", hiring, " Lawyers for $", cost, sep='')
    input_buffer()

def fire_lawyers(world):
    lawyers = world.lawyers
    count = lawyers.count

    print("Lawyers on the books:", count)

    firing = valid_numeric_input(
        "How many Lawyers are we firing", 0, count, 0
    )

    lawyers.count -= firing

    print(firing, "Lawyers fired")
    input_buffer()


def new_city(world):
    ply = world.player
    cost = world.city_cost

    if ply.money < cost:
        print("We need at least $", cost, " to build another City", sep='')
    else:
        print("\nBuilding a new City will cost $", cost, sep='')
        print("We need a name for it. Hit enter with no name to cancel")
        name = input("\nWhat will be the name of our new city: ")

        world.add_city(name)
        world.city_cost *= 2

        print("\nPleasure doing business with you")
        print("We will have", name, "built immediately")
    
    input_buffer()

menu_gov_trade = Menu(
    "Goverment Trades", "What sort of business do you have with us", [
        Option("Make Shady Donation", '', 'd', shady_donation),
        Option("Hire Lawyers", '', 'l', hire_lawyers),
        Option("Fire Lawyers", '', 'f', fire_lawyers),
        Option("Purchase new City", '', 'c', new_city)
    ]
)

def leave_casino():
    print(casino_phrase())
    input_buffer()

def get_gambling_pot(world):
    return valid_numeric_input(
        "How much money would you like to put in your gambling pot",
        0, world.player.money, min(world.player.money, 100000)
    )

def casino_game(world, game_obj):
    ply = world.player
    pot = get_gambling_pot(world)

    if pot == 0:
        leave_casino()
        return
    
    ply.money -= pot

    system("cls")
    game = game_obj(pot)
    ply.money += game.play(world)
    leave_casino()

def casino_bingo(world):
    from minigames.bingo import Bingo
    casino_game(world, Bingo)

def casino_blackjack(world):
    from minigames.blackjack import Blackjack
    casino_game(world, Blackjack)

def casino_horse_racing(world):
    from minigames.horse_betting import HorseBetting
    casino_game(world, HorseBetting)

def casino_double_or_nothing(world):
    from minigames.double_nothing import DoubleOrNothing
    casino_game(world, DoubleOrNothing)

menu_casino = Menu(
    "Casino", "What game would you like to play", [
        Option("Bingo", '', 'n', casino_bingo),
        Option("Blackjack", '', 'b', casino_blackjack),
        Option("Horse Racing", '', 'h', casino_horse_racing),
        Option("Double or Nothing", '', 'd', casino_double_or_nothing)
    ]
)

menu_shopping = Menu(
    "Shopping and Commerce", "Where would you like to go", [
        Option("Buy Gear", "menu_buy_gear", 'g'),
        Option("Visit Bank", "menu_bank", 'b'),
        Option("Government Trades", "menu_gov_trade", 't'),
        Option("Visit Casino", "menu_casino", 'c'),
    ]
)
