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
    mission_crew = prepare_crime(world, "Robbing Pedestrians", 500)
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

def check_crew_size(world, requirement):
    if len(world.player.crew) < requirement:
        print(f"You need at least {requirement} Crew Members for a job like that!")
        input_buffer()
        return False
    return True

def confirm_heist(name, crew_count, reward, failure):
    print(name, '\n')
    print(f"Crew needed: {crew_count}")
    print("Reward:", reward)
    print("Failure:", failure)

    print("\nAre you sure you want to go through with this Heist?")
    choice = None

    while choice == None:
        try: choice = input("(y or n): ")[0].lower()
        except: continue

        if choice == 'y': return True
        elif choice == 'n': return False
        else: print("Invalid choice\n")

def redeposit_crew(world, crew):
    if crew == None: return
    for id in crew: world.player.crew[id] = crew[id]

def heist_bank(world):
    confirm = check_crew_size(world, 50)
    if not confirm: return

    confirm = confirm_heist(
        "Bank Heist", 50, "Lots of Cash and Gold",
        "Massive retaliation from the Police and the Financial Sector"
    )

    if not confirm: return

    from heists.heist_bank import HeistBank
    target = HeistBank()
    target.load_crew(world)
    survived = target.start(world)
    redeposit_crew(world, survived)

def heist_prison(world):
    confirm = check_crew_size(world, 100)
    if not confirm: return

    confirm = confirm_heist(
        "Prison Break", 100, "Many new Crew Members",
        "Your Crew can get locked up easily in a Prison"
    )

    if not confirm: return

    from heists.heist_prison import HeistPrison
    target = HeistPrison()
    target.load_crew(world)
    survived = target.start(world)
    redeposit_crew(world, survived)

menu_heist = Menu(
    "Planning Heist", "What's the plan Boss", [
        Option("Bank Heist", '', 'b', heist_bank),
        Option("Prison Break", '', 'p', heist_prison)
    ]
)

def hack_police(world):
    ply = world.player
    measure = ply.heat

    if measure == 0:
        print("You don't have any kind of record to wipe clean")
        input_buffer()
        return

    from minigames.memory_injection import MemoryInjection

    difficulty = 1

    while difficulty < 10 and measure > 0:
        measure //= 10
        difficulty += 1
    
    game = MemoryInjection(difficulty)
    discovered = game.play()

    if discovered: ply.heat *= rand(2, 4)
    else: ply.heat = int(ply.heat * 0.4)


menu_crime = Menu(
    "Commit Crime", "What kind of job are we doing", [
        Option("Petty Crime", "menu_crime_petty", 'p'),
        Option("Start Heist", "menu_heist", 'h'),
        Option("Hack Police Computers", '', 'a', hack_police)
    ]
)
