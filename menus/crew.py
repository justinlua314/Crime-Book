from prettytable import PrettyTable

from menu import Menu, Option, input_buffer, coming_soon

def crew_summary(world):
    ply = world.player
    buckets = {} # weapon_name : [member_count, average_health, average_armor]

    for member in ply.crew.values():
        wep_id = ("Fists" if member.weapon == None else member.weapon.name)

        if wep_id not in buckets.keys():
            buckets[wep_id] = [1, member.health, member.armor]
        else:
            buckets[wep_id][0] += 1
            buckets[wep_id][1] += member.health
            buckets[wep_id][2] += member.armor
    
    for _,bucket in buckets.items():
        bucket[1] = int(bucket[1] / bucket[0])
        bucket[2] = int(bucket[2] / bucket[0])

    print('$' + str(ply.money) + '\n')
    render = PrettyTable()
    render.field_names = ["Crew Weapon", "Count", "Average Health", "Average Armor"]

    for wep, data in buckets.items():
        render.add_row([wep, data[0], data[1], data[2]], divider=True)

    print(f"\n{render}")
    input_buffer()


def print_stats(world, group):
    world.stats.refresh_stats(world)
    render = PrettyTable()
    render.field_names = ["Statistic", "Value"]

    for stat in world.stats.data[group].values():
        value = stat.count
        if stat.money: value = (f"${value}")

        render.add_row([stat.description, value], divider=True)
    
    print(render)
    input_buffer()

def stats_general(world): print_stats(world, "General")
def stats_crime(world): print_stats(world, "Crime")
def stats_shopping(world): print_stats(world, "Shopping")
def stats_banking(world): print_stats(world, "Banking / Government")
def stats_casino(world): print_stats(world, "Casino")
def stats_territories(world): print_stats(world, "Territories")
def stats_business(world): print_stats(world, "Business")
def stats_export(world): world.stats.export_stats(world)

menu_stats = Menu(
    "Game Stats", "Select stat category", [
        Option("General", '', 'g', stats_general),
        Option("Crime", '', 'c', stats_crime),
        Option("Shopping", '', 's', stats_shopping),
        Option("Banking / Government", '', 'b', stats_banking),
        Option("Casino", '', 'a', stats_casino),
        Option("Territories", '', 't', stats_territories),
        Option("Business", '', 'u', stats_business),
        Option("Export stats to txt file", '', 'e', stats_export)
    ]
)

def crew_skills(world):
    ply = world.player
    buckets = {} # weapon_name : [member_count, average_stats...]

    for member in ply.crew.values():
        wep_id = ("Fists" if member.weapon == None else member.weapon.name)

        if wep_id not in buckets.keys():
            buckets[wep_id] = [1]

            for stat in member.stats.values():
                buckets[wep_id].append(stat[0])
        else:
            buckets[wep_id][0] += 1

            for index, stat in enumerate(member.stats.values()):
                buckets[wep_id][index + 1] += stat[0]

    average_data = {}

    for wep_id, data in buckets.items():
        average_data[wep_id] = []

        for index, skill in enumerate(data[1:]):
            average_data[wep_id].append(skill // data[0])

    render = PrettyTable()
    render.field_names = [
        "Crew Weapon", "Count", "Accuracy",
        "Dodging", "Shooting", "Strength"
    ]

    for wep_id, data in average_data.items():
        render.add_row([wep_id, buckets[wep_id][0]] + data, divider=True)
    
    print(render)
    input_buffer()


menu_crew = Menu(
    "Inspect and Manage Crew", "What would you like to know", [
        Option("Crew Summary", '', 'c', crew_summary),
        Option("Game Statistics", "menu_stats", 's'),
        Option("Average Crew Skills", '', 'k', crew_skills)
    ]
)
