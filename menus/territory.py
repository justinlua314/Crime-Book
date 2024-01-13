from os import system
from prettytable import PrettyTable
from random import sample

from menu import Menu, Option, input_buffer, valid_numeric_input, coming_soon
from menus.crime import prepare_crime


def select_city(world, prompt):
    system("cls")
    render = PrettyTable()
    render.field_names = ["Key", "Name", "Gang Economy", "Top Gang", "Crew Members"]

    render.add_row([0, "Cancel", "NA", "NA", "NA"], divider=True)

    for index, city in enumerate(world.cities.values()):
        render.add_row([
            (index + 1), city.name, city.gang_economy(),
            city.top_gang(), city.crew_population()
        ], divider=True)
    
    print(render)
    choice = valid_numeric_input(prompt, 0, len(world.cities), 0)

    if choice == 0: return None
    return world.cities[list(world.cities.keys())[choice - 1]]


def select_block(city, prompt):
    system("cls")
    render = PrettyTable()
    render.field_names = [
        "Block Number", "Gang Economy", "Top Gang", "Crew Members"
    ]

    render.add_row([0, "Cancel", "NA", "NA"], divider=True)

    for index, block in enumerate(city.blocks):
        render.add_row([
            (index + 1), block.gang_economy(),
            block.controlling_gang().name, block.crew_population()
        ], divider=True)
    
    print(render)
    choice = valid_numeric_input(prompt, 0, len(city.blocks), 1)

    if choice == 0: return
    return city.blocks[choice - 1]


def target_block(world):
    print("Block Takeover")

    city = select_city(world, "\nWhich City are we hitting")
    if city == None: return
    
    block = select_block(city, "\nWhich Block are we hitting")
    if block == None: return

    block_number = -1

    for index, scan in enumerate(city.blocks):
        if scan is block:
            block_number = index + 1
            break

    crew = prepare_crime(world, '', 1000)
    if len(crew) == 0: return
    block.add_crew_members(world, crew)

    print(f"\n{len(crew)} Crew Members sent to {city.name} Block #{block_number}")
    input_buffer()

def city_takeover(world):
    print("City Takeover")

    city = select_city(world, "\nWhich City are we taking over")
    if city == None: return

    crew = prepare_crime(
        world, "\nHow many Crew Members are we sending to this City", 10000
    )
    if len(crew) == 0: return

    city.send_crew(world, len(crew))

    print(f"\n{len(crew)} Crew Members sent to take over {city.name}")
    input_buffer()

def world_takeover(world):
    print("Scatter Strategy")

    crew = prepare_crime(
        world, "How many Crew Members are we sending to cause chaos?", 25000
    )
    if len(crew) == 0: return

    world.send_crew(len(crew))

    print(f"\n{len(crew)} Crew Members sent to choas havoc on the World")
    input_buffer()


menu_strategy = Menu(
    "Territory Strategy", "What's our plan for taking over", [
        Option("Target specific Block", '', 'b', target_block),
        Option("Take over City", '', 'c', city_takeover),
        Option("Take over World", '', 'w', world_takeover),
    ]
)



def retract_crew_block(world):
    city = select_city(world, "\nWhich City has the block we're looking for")
    if city == None: return

    block = select_block(city, "\nWhich Block are we retracting from")
    amount = block.crew_population()
    block.evacuate_crew(world)

    print(amount, "Crew Members evacuated")
    input_buffer()

def retract_crew_city(world):
    city = select_city(world, "\nWhich City are we evacuating")
    if city == None: return

    amount = city.crew_population()
    city.evacuate_crew(world)

    print(amount, "Crew Members evacuated")
    input_buffer()

def retract_crew_world(world):
    amount = world.crew_population()
    world.evacuate_crew()

    print("All", amount, "Crew Members evacuated")
    input_buffer()

menu_withdraw_crew = Menu(
    "Wtihdraw Crew Members from the Streets", "How many people are we bringing back?", [
        Option("Retract from Block", '', 'b', retract_crew_block),
        Option("Retract from City", '', 'c', retract_crew_city),
        Option("Retract all Crew Members", '', 'w', retract_crew_world)
    ]
)



def view_coffer(world):
    print(f"Gang Coffer: ${world.gang_coffer}")
    print(f"Money needed by your Gangs: ${world.gang_deficite()}\n")
    print(f"Money: ${world.player.money}")
    input_buffer()

def deposit_coffer(world):
    print(f"Gang Coffer: ${world.gang_coffer}")
    print(f"Money needed by your Gangs: ${world.gang_deficite()}\n")

    ply = world.player
    donation = valid_numeric_input(
        "How much money would you like to donate", 0, ply.money, (ply.money // 2)
    )

    if donation > 0:
        world.gang_coffer += donation
        ply.money -= donation

        print(f"${donation} donation deposited")
        input_buffer()

def withdraw_coffer(world):
    print(f"Gang Coffer: ${world.gang_coffer}")
    print(f"Money needed by your Gangs: ${world.gang_deficite()}")

    ply = world.player
    withdraw = valid_numeric_input(
        "How much money would you like to withdraw", 0,
        world.gang_coffer, (world.gang_coffer // 2)
    )

    if withdraw > 0:
        ply.money += withdraw
        world.gang_coffer -= withdraw

        print(f"${withdraw} withdrawn")
        input_buffer()

def set_gang_cap(world):
    print("If a gang controlled by you has more money than the cap, they will donate the excess funds back to your money coffer.")
    print(f"\nGang Cap: ${world.gang_money_cap}")

    new_cap = valid_numeric_input(
        "What would you like the new cap to be", 0, 100000, 5000
    )

    if new_cap == 0: return

    world.gang_money_cap = new_cap

    print(f"New gang money cap is ${world.gang_money_cap}")
    input_buffer()


menu_coffer = Menu(
    "Money Coffers", "What's our budget looking like", [
        Option("View Cash Balance", '', 'c', view_coffer),
        Option("Deposit Money", '', 'd', deposit_coffer),
        Option("Withdraw Money", '', 'w', withdraw_coffer),
        Option("Set Gang Money Cap", '', 's', set_gang_cap)
    ]
)


def inspect_world(world):
    city = select_city(world, "Which city would you like to check out?")
    if city == None: return
    system("cls")

    render = PrettyTable()
    render.field_names = [
        "Block #", "Controlling Gang", "Top Gangs Wealth",
        "Total Economy", "Average Gang Size", "Crew Members"
    ]

    for id, block in enumerate(city.blocks):
        top = block.controlling_gang()
        render.add_row([
            id + 1, top.name, top.money, block.gang_economy(), block.average_crew_size(), block.crew_population()
        ], divider=True)
    
    print(render)
    input_buffer()


menu_territory = Menu(
    "Manage Territory", "What's the plan Boss", [
        Option("Control Territories", "menu_strategy", 't'),
        Option("Retract Crew Members", "menu_withdraw_crew", 'r'),
        Option("Inspect World Map", '', 'w', inspect_world),
        Option("Manage Money Coffer", "menu_coffer", 'c')
    ]
)
