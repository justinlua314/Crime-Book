from prettytable import PrettyTable

from menu import Menu, Option, input_buffer, coming_soon

def inspect_gear(world):
    ply = world.player

    print("Money: $" + str(ply.money))

    render = PrettyTable()
    render.field_names = ["Resource", "Quantity Available"]
    render.add_row(["Vests", ply.vests], divider=True)

    for id,count in ply.weapons.items():
        weapon_name = world.weapons.lookup_weapon(id).name
        render.add_row([weapon_name, count], divider=True)
    
    print(render)
    input_buffer()

def distribute_armor(world):
    world.player.distribute_vests()
    print("\nArmor Distributed")
    input_buffer()

def distribute_weapons(world):
    world.player.distribute_arms(world)
    print("\nWeapons Distributed")
    input_buffer()

def inspect_warehouse(world): world.warehouse.inspect_inventory()
def sell_warehouse_items(world): world.warehouse.sell_items(world)

def car_money(world):
    print("Car Shop\n")
    shop = world.car_shop
    print(f"Cars in car shop: {shop.car_count()}")
    payment = shop.money

    if payment == 0:
        if len(shop.cars) == 0:
            print("We don't have any cars! Go jack some for us if you want money")
        else:
            print("We haven't sold anything yet! Come back later")
    else:
        shop.money = 0
        world.player.money += payment
        print(f"${payment} paid out by the Car Shop")

    input_buffer()


menu_warehouse = Menu(
    "Criminal Warehouse", "What would you like to see boss", [
        Option("Inspect Gear", '', 'g', inspect_gear),
        Option("Inspect Warehouse Inventory", '', 'i', inspect_warehouse),
        Option("Sell Warehouse Items", '', 's', sell_warehouse_items),
        Option("Collect Money from Car Shop", '', 'c', car_money),
        Option("Distribute Armor", '', 'a', distribute_armor),
        Option("Distribute Weapons", '', 'w', distribute_weapons)
    ]
)
