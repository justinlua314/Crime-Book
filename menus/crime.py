from random import sample
from random import randint as rand

from menu import Menu, Option, crew_count_input, input_buffer
from events import EventLog
from objects.humans import Ped, Cop
from objects.warehouse import Item
from resources.loot_tables import roll_random_car, roll_household_item

def prepare_crime(world, title, max_crew):
    print(title)

    ply = world.player
    count = crew_count_input(ply, max_crew)
    return sample(sorted(ply.crew), count)

def rob_pedestrian(world):
    log = EventLog()
    mission_crew = prepare_crime(world, "Robbing Pedestrians", 5000)
    if len(mission_crew) == 0: return
    ply = world.player

    for id in mission_crew:
        member = ply.crew[id]
        target = (Cop(world) if rand(1, 20) == 10 else Ped(world, True))
        member.fight(target, world, log)

    log.print_events()
    input_buffer()

def car_jacking(world):
    log = EventLog()
    mission_crew = prepare_crime(world, "Stealing Cars", 200)
    if len(mission_crew) == 0: return
    give = world.car_shop.give_car

    for id in mission_crew:
        member = world.player.crew[id]
        cop = (rand(1, 50) == 10)

        if cop:
            member.fight(Cop(world), world, log)

            if member.alive():
                log.log("copcar_stolen", "Cop Cars Stolen")
                give(Item("cop_car", "Cop Car", 7000, rand(2, 4)))
                world.player.heat += 3
        else:
            for i in range(rand(1, 4)):
                if rand(1, (10 * (5 * i+1))) == 5 and member.alive():
                    member.fight(Ped(world, True), world, log)
            
            if member.alive():
                car = roll_random_car()
                id = (car.id + "_stolen")
                log.log(id, car.name + " Stolen")
                give(roll_random_car())
                world.player.heat += (2 * rand(0, 1))

    log.print_events()

    print("\nYour cars are stored in the Car Shop where they will be sold off")
    input_buffer()

def house_robbery(world):
    log = EventLog()
    mission_crew = prepare_crime(world, "House Robbery", 100)
    if len(mission_crew) == 0: return
    give = world.warehouse.give_item
    ply = world.player

    for id in mission_crew:
        member = ply.crew[id]
        greed = rand(1, 4)
        residence_killed = False

        for i in range(1, greed+1):
            item = roll_household_item()

            if rand(1, 5) == 5 and not residence_killed:
                for _ in range(rand(1, 2)):
                    armed = (True if rand(1, 4) == 4 else False)
                    member.fight(Ped(world, armed), world, log)

                    if not member.alive(): break
            
            if not member.alive(): break
            
            if i == 3 and rand(1, 30) == 15:
                member.fight(Cop(world), world, log)
            
            if i == 4 and rand(1, 5) != 1 and member.alive():
                for _ in range(rand(2, 8)):
                    member.fight(Cop(world), world, log)

                    if not member.alive(): break
            
            if member.alive(): give(item)
            else:
                if i == 3: ply.heat += 10
                elif i == 4: ply.heat += 25
                break
    
    log.print_events()

    print("\nWe'll store these items in the Warehouse. Sell them whenever you like")
    input_buffer()


menu_crime_petty = Menu(
    "Commit Petty Crime", "What's our target", [
        Option("Rob Pedestrian", '', 'r', rob_pedestrian),
        Option("Jacking Cars", '', 'c', car_jacking),
        Option("Robbing Houses", '', 'h', house_robbery)
    ]
)

menu_crime = Menu(
    "Commit Crime", "What kind of job are we doing", [
        Option("Petty Crime", "menu_crime_petty", 'p')
    ]
)
