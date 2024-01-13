from random import sample
from random import randint as rand

from menu import Menu, Option, input_buffer, crew_count_input, valid_numeric_input
from events import EventLog
from objects.humans import Ped, Cop

def recruit_campaign(world, strategy=0):
    match(strategy):
        case 0: print("Alright, we're recuiting pedestrians")
        case 1: print("They will join the crew whether they want to or not")
        case 2: print("Let's show them the kind of money we make around here")

    ply = world.player

    count = crew_count_input(ply, 500, False)
    if count == 0: return

    if strategy == 2:
        while count > ply.money:
            print("You don't have enough money to send that many members bribing")
            count = valid_numeric_input(
                "How many crew members do we send", 1, ply.money, ply.money
            )

        print("\n\nWhat is our total budget for bribing?")
        print("This amount will be split across", count, "crew members\n")
        default = min(ply.money, (count * 10000))
        total_budget = valid_numeric_input("Total budget", 1, ply.money, default)
        budget = (total_budget // count)

        while budget == 0: # Might not actually get called
            print("That's too many people and not enough money.")
            total_budget = valid_numeric_input("Total budget", 1, ply.money, ply.money)
            budget = (total_budget // count)

        ply.money -= total_budget

        print("\nSending", count, "crew members out with $" + str(budget), "each")

    log = EventLog()

    if strategy == 1:
        best_power = []
        lowest = 9999

        for id, member in ply.crew.items():
            power = member.power_level()

            if len(best_power) < count:
                best_power.append([id, power])
                if power < lowest: lowest = power
            else:
                # Doesn't necessarily pull the absolute best people, but simple alg
                for top in best_power:
                    if power > top[1]:
                        top[0] = id
                        top[1] = power
                        if power < lowest: lowest = power
                        break
            
        crew_members = {}

        # Might be too slow. Hopefully lowest variable speeds things up a bit
        for _, member in ply.crew.items():
            power = member.power_level()
            if power < lowest: continue

            for top in best_power:
                if power == top[1]: crew_members[top[0]] = member
    else:
        crew_members = sample(sorted(ply.crew), count)

    money_returned = 0

    for id in crew_members:
        if rand(1, 80) == 10: target = Cop(world)
        else: target = Ped(world)

        member = ply.crew[id]

        match(strategy):
            case 0: member.recruit(target, world, log)
            case 1: member.intimidate(target, world, log)
            case 2: money_returned += member.bribe(target, budget, world, log)
    
    if strategy == 2:
        log.log("money_returned", "Money recovered", money_returned)
        ply.money += money_returned
    
    print()
    log.print_events()
    input_buffer()

def recruit_peds(world): recruit_campaign(world, 0)
def intimidate_peds(world): recruit_campaign(world, 1)
def bribe_peds(world): recruit_campaign(world, 2)

menu_recruit = Menu(
    "Recruit Crew Members", "What's our recruitment strategy?", [
        Option("Approach Pedestrians", '', 'p', recruit_peds),
        Option("Intimidate Pedestrians", '', 'i', intimidate_peds),
        Option("Bribe Pedestrians", '', 'b', bribe_peds)
    ]
)
