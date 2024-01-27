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
def cheat_busted(world): world.player.heat = (world.player.heat_cap + 1)

def cheat_time_warp(world):
    print("Warping 50 turns into the future")
    for _ in range(50): world.think(False)

def cheat_world_domination(world):
    print("Taking over World")
    amount = (9000 * len(world.cities))
    world.player.give_random_crew_members(world, amount)
    world.send_crew(amount)
    world.gang_coffer = max(world.gang_coffer, 1000000000)

def cheat_debug(world):
    stats = world.stats
    stats.refresh_stats(world)

    for stat in stats.data["Business"].values():
        print(stat.description, stat.count)
    
    input("\nPress enter to continue")



cheat_codes = {
    "block party"       : cheat_block_party,
    "new money"         : cheat_new_money,
    "factorial money"   : cheat_fact_money,
    "layoff"            : cheat_layoff,
    "undercover"        : cheat_undercover,
    "rosenberg"         : cheat_rosenberg,
    "ilose"             : cheat_ilose,
    "busted"            : cheat_busted,
    "timewarp"          : cheat_time_warp,
    "world domination"  : cheat_world_domination,
    "debug"             : cheat_debug
}
