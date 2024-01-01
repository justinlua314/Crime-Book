def factorial(n):
    if n < 3: return n
    else: return n * factorial(n-1)

def cheat_block_party(world): world.player.give_random_crew_members(world, 500)
def cheat_new_money(world): world.player.money += 1000000000
def cheat_fact_money(world): world.player.money = factorial(50)
def cheat_layoff(world): world.player.heat = 0
def cheat_undercover(world): world.player.heat_cap = 1000000000
def cheat_rosenberg(world): world.lawyers.count = world.lawyers.max_count
def cheat_ilose(world):
    world.evacuate_crew()
    world.player.crew.clear()

def cheat_debug(world):
    for city_name, city in world.cities.items():
        for block in city.blocks:
            for gang in block.gangs:
                if not gang.ai: print(city_name, len(gang.crew))

    input("\n\nPress enter to continue")



cheat_codes = {
    "block party"       : cheat_block_party,
    "new money"         : cheat_new_money,
    "factorial money"   : cheat_fact_money,
    "layoff"            : cheat_layoff,
    "undercover"        : cheat_undercover,
    "rosenberg"         : cheat_rosenberg,
    "ilose"             : cheat_ilose,
    "debug"             : cheat_debug
}
