from os import system

from objects.world import World
from menu import MenuManager, valid_numeric_input, input_buffer, coming_soon

from menus.home import menu_home
from menus.crime import menu_crime, menu_crime_petty, rob_pedestrian, car_jacking, house_robbery
from menus.territory import menu_territory, menu_strategy, menu_withdraw_crew, menu_coffer, target_block, city_takeover, world_takeover, retract_crew_block, retract_crew_city, retract_crew_world, view_coffer, deposit_coffer, withdraw_coffer, inspect_world
from menus.shopping import menu_shopping, menu_buy_gear, menu_gov_trade, menu_casino, shop_buy_bat, shop_buy_armor, shop_buy_pistol, shop_buy_shotgun, shop_buy_rifle, shady_donation, hire_lawyers, new_city, casino_blackjack, casino_horse_racing
from menus.wh import menu_warehouse, inspect_gear, inspect_warehouse, sell_warehouse_items, distribute_armor, distribute_weapons, car_money
from menus.crew import menu_crew, crew_summary, crew_skills
from menus.recruit import menu_recruit, recruit_peds, intimidate_peds, bribe_peds

class CrimeGame:
    def __init__(self):
        self.gang_name = "My Crew"
        self.world = World()
        # Menus cannot be accessed until they are registered here
        self.menu_manager = MenuManager("menu_home", {
            "menu_home" : menu_home,
            "menu_crime" : menu_crime,
            "menu_crime_petty" : menu_crime_petty,
            "menu_territory" : menu_territory,
            "menu_strategy" : menu_strategy,
            "menu_withdraw_crew" : menu_withdraw_crew,
            "menu_coffer" : menu_coffer,
            "menu_shopping" : menu_shopping,
            "menu_buy_gear" : menu_buy_gear,
            "menu_gov_trade" : menu_gov_trade,
            "menu_casino" : menu_casino,
            "menu_warehouse" : menu_warehouse,
            "menu_crew" : menu_crew,
            "menu_recruit" : menu_recruit
        },
        
        {   # Macros to navigate menus faster
            "cpr" : rob_pedestrian,
            "cpc" : car_jacking,
            "cph" : house_robbery,
            "ttb" : target_block,
            "ttc" : city_takeover,
            "ttw" : world_takeover,
            "trb" : retract_crew_block,
            "trc" : retract_crew_city,
            "trw" : retract_crew_world,
            "tw"  : inspect_world,
            "tcc" : view_coffer,
            "tcd" : deposit_coffer,
            "tcw" : withdraw_coffer,
            "sgb" : shop_buy_bat,
            "sga" : shop_buy_armor,
            "sgp" : shop_buy_pistol,
            "sgs" : shop_buy_shotgun,
            "sgr" : shop_buy_rifle,
            "std" : shady_donation,
            "stl" : hire_lawyers,
            "stc" : new_city,
            "scb" : casino_blackjack,
            "sch" : casino_horse_racing,
            "wg"  : inspect_gear,
            "wi"  : inspect_warehouse,
            "ws"  : sell_warehouse_items,
            "wa"  : distribute_armor,
            "ww"  : distribute_weapons,
            "wc"  : car_money,
            "ic"  : crew_summary,
            "is"  : crew_skills,
            "rp"  : recruit_peds,
            "ri"  : intimidate_peds,
            "rb"  : bribe_peds,
        })

    def lose(self):
        print("There's no more Crew Members backing you")
        print("\nThe Streets are full, but with the wrong guys")
        print("\nTime for you to go join them yourself.")

        print("\n\nAm I really not Mob Boss material?\n")
        print("1. Give me another chance, 10 more guys, no money needed. (Play Again)")
        print("2. Time to become a Pedestrian (Quit Game)")

        answer = valid_numeric_input("\nYour response", 1, 2, 2)

        if answer == 1:
            print("\nDammit, okay I'll see what kind of strings I can pull")
            print("Do NOT mess this operation up again!!")
            self.world = World()
            input_buffer()
            return True
        
        return False

    def get_gang_name(self):
        system("cls")
        print("What's the name of our new Crew?")
        sure = False

        while not sure:
            name = input("\nWe are The ")
            print("\nThe ", name, ", is that right?", sep='')
            print("\nPress y to confirm. Hit enter to try again")
            sure = (True if input().lower() == 'y' else False)

    # Main game loop
    def play(self):
        self.world.player_gang_name = self.get_gang_name()
        playing = True

        while playing:
            before_heat = self.world.player.heat
            playing, should_think = self.menu_manager.prompt(self.world)
            after_heat = self.world.player.heat

            if should_think: self.world.think(before_heat != after_heat)

            if len(self.world.player.crew) == 0 and self.world.crew_population() == 0:
                playing = self.lose()
        
        system("cls")
        print("Thank you for playing Crime Book")
