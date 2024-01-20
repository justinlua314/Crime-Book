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
    world.stats.add_stat("gear_money", (qty * 100))
    world.stats.add_stat("vests_purchased", qty)

shop_weapons = ["bat", "pistol", "shotgun", "rifle"]

def shop_buy_weapon(world, index):
    wep = world.weapons.lookup_weapon(shop_weapons[index])
    before_money = world.player.money
    qty = purchase(world, wep.price, shop_purchase_qty(world, wep.price))
    world.player.give_weapon(wep.id, qty)
    world.stats.add_stat("gear_money", (before_money - world.player.money))
    world.stats.add_stat(f"{shop_weapons[index]}s_purchased", qty)

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
def bank_auto_withdraw(world): world.bank.change_auto_withdraw(world)
def bank_take_loan(world): world.bank.take_loan(world)
def bank_pay_loan(world): world.bank.pay_loan(world)


menu_bank = Menu(
    "The Bank", "How can we help you sir", [
        Option("Deposit Money", '', 'd', bank_deposit),
        Option("Withdraw Money", '', 'w', bank_withdraw),
        Option("Set up Auto Withdraw", '', 'a', bank_auto_withdraw),
        Option("Request Loan", '', 'l', bank_take_loan),
        Option("Make Loan Payment", '', 'p', bank_pay_loan)
    ]
)


def buy_food(world):
    ply = world.player
    hungry = ply.get_hungry_crew()

    if hungry == 0:
        print("None of your crew members are hungry")
        input_buffer()
        return

    if ply.money < 50:
        print("You can't afford to feed any of your Crew Members :(")
        input_buffer()
        return

    print(f"Money: ${ply.money}")
    print("Food Ration: $50")
    print(f"Hungry Crew Members: {hungry}")

    maximum = min((ply.money // 50), hungry)
    qty = valid_numeric_input("\nHow many meals are we buying?", 0, maximum, maximum)
    if qty == 0: return

    price = qty * 50
    ply.money -= price
    ply.feed_crew(qty)
    world.stats.add_stat("rations_eaten", qty)

    print(f"{qty} Crew Members fed for ${price}")
    input_buffer()


def shady_donation(world):
    ply = world.player
    print(f"Money: ${ply.money}")

    donation = valid_numeric_input(
        "How much money are we forking over", 0, ply.money, (ply.money // 2)
    )
    if donation == 0: return

    ply.money -= donation
    heat_change = (donation // (ply.heat_cap // 10))
    ply.heat_cap += heat_change
    world.stats.add_stat("fed_money", donation)
    world.stats.max_stat("heat_cap_high", ply.heat_cap)

    print(f"${donation} donated to the feds")
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
            print(f"You can't afford any Lawyers, They're ${cost} a pop!")

        input_buffer()
        return

    print(f"Cost per Lawyer: ${cost} ever {lawyers.turns} turns")
    print("\nLawyers on the books:", lawyers.count)
    print(f"Current cost every {lawyers.turns} turns: ${cost * count}")

    print(f"\nMoney: ${ply.money}")

    hiring = valid_numeric_input(
        "\nHow many Lawyers are we hiring", 0, can_afford, 0
    )

    if hiring == 0: return

    lawyers.count += hiring
    cost *= hiring
    ply.money -= cost

    print(f"\nHired {hiring} Lawyers for ${cost}")
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
        print(f"We need at least ${cost} to build another City")
    else:
        print(f"\nBuilding a new City will cost ${cost}")
        print("We need a name for it. Hit enter with no name to cancel")
        name = input("\nWhat will be the name of our new city: ")

        world.add_city(name)
        world.city_cost *= 2
        world.stats.inc_stat("cities_purchased")

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
    after_pot = game.play(world)
    ply.money += after_pot
    world.stats.add_stat("winnings", max(after_pot - pot, 0))

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

def casino_fortune_wheel(world):
    from minigames.fortune_wheel import FortuneWheel
    casino_game(world, FortuneWheel)

menu_casino = Menu(
    "Casino", "What game would you like to play", [
        Option("Bingo", '', 'i', casino_bingo),
        Option("Blackjack", '', 'b', casino_blackjack),
        Option("Horse Racing", '', 'h', casino_horse_racing),
        Option("Double or Nothing", '', 'd', casino_double_or_nothing),
        Option("Wheel of Fortune", '', 'w', casino_fortune_wheel)
    ]
)

menu_shopping = Menu(
    "Shopping and Commerce", "Where would you like to go", [
        Option("Buy Gear", "menu_buy_gear", 'g'),
        Option("Buy Food", '', 'f', buy_food),
        Option("Visit Bank", "menu_bank", 'b'),
        Option("Government Trades", "menu_gov_trade", 't'),
        Option("Visit Casino", "menu_casino", 'c'),
    ]
)
