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

    print('\n', render, sep='')
    input_buffer()

def crew_skills(world): # Unfinished
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

        for skill in range(1, len(data)):
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
        Option("Average Crew Skills", '', 's', crew_skills)
    ]
)
