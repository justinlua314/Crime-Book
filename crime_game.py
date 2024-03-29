from os import system
from prettytable import PrettyTable

from objects.world import World
from objects.tutorial import Tutorial
from menu import MenuManager, input_buffer, flush_input

from menus.home import menu_home
from menus.save import load_game

import menus.crime as Crime
import menus.territory as Territory
import menus.shopping as Shopping
import menus.wh as Warehouse
import menus.crew as Crew
import menus.recruit as Recruit
import menus.busy as Business
import menus.save as Save

class CrimeGame:
    def __init__(self):
        self.world = World()
        # Menus cannot be accessed until they are registered here
        self.menu_manager = MenuManager("menu_home", {
            "menu_home"             : menu_home,
            "menu_crime"            : Crime.menu_crime,
            "menu_crime_petty"      : Crime.menu_crime_petty,
            "menu_heist"            : Crime.menu_heist,
            "menu_territory"        : Territory.menu_territory,
            "menu_strategy"         : Territory.menu_strategy,
            "menu_withdraw_crew"    : Territory.menu_withdraw_crew,
            "menu_coffer"           : Territory.menu_coffer,
            "menu_shopping"         : Shopping.menu_shopping,
            "menu_buy_gear"         : Shopping.menu_buy_gear,
            "menu_bank"             : Shopping.menu_bank,
            "menu_gov_trade"        : Shopping.menu_gov_trade,
            "menu_casino"           : Shopping.menu_casino,
            "menu_warehouse"        : Warehouse.menu_warehouse,
            "menu_crew"             : Crew.menu_crew,
            "menu_stats"            : Crew.menu_stats,
            "menu_recruit"          : Recruit.menu_recruit,
            "menu_business"         : Business.menu_business,
            "menu_save"             : Save.menu_save
        },
        
        {   # Macros to navigate menus faster
            "cpr" : Crime.rob_pedestrian,
            "cpc" : Crime.car_jacking,
            "cph" : Crime.house_robbery,
            "chb" : Crime.heist_bank,
            "chp" : Crime.heist_prison,
            "ca"  : Crime.hack_police,
            "ttb" : Territory.target_block,
            "ttc" : Territory.city_takeover,
            "ttw" : Territory.world_takeover,
            "trb" : Territory.retract_crew_block,
            "trc" : Territory.retract_crew_city,
            "trw" : Territory.retract_crew_world,
            "tw"  : Territory.inspect_world,
            "tcc" : Territory.view_coffer,
            "tcd" : Territory.deposit_coffer,
            "tcw" : Territory.withdraw_coffer,
            "sgb" : Shopping.shop_buy_bat,
            "sga" : Shopping.shop_buy_armor,
            "sgp" : Shopping.shop_buy_pistol,
            "sgs" : Shopping.shop_buy_shotgun,
            "sgr" : Shopping.shop_buy_rifle,
            "sf"  : Shopping.buy_food,
            "sbd" : Shopping.bank_deposit,
            "sbw" : Shopping.bank_withdraw,
            "sba" : Shopping.bank_auto_withdraw,
            "sbl" : Shopping.bank_take_loan,
            "sbp" : Shopping.bank_pay_loan,
            "std" : Shopping.shady_donation,
            "stl" : Shopping.hire_lawyers,
            "stf" : Shopping.fire_lawyers,
            "stc" : Shopping.new_city,
            "sci" : Shopping.casino_bingo,
            "scb" : Shopping.casino_blackjack,
            "sch" : Shopping.casino_horse_racing,
            "scd" : Shopping.casino_double_or_nothing,
            "scw" : Shopping.casino_fortune_wheel,
            "wg"  : Warehouse.inspect_gear,
            "wi"  : Warehouse.inspect_warehouse,
            "ws"  : Warehouse.sell_warehouse_items,
            "wa"  : Warehouse.distribute_armor,
            "ww"  : Warehouse.distribute_weapons,
            "wc"  : Warehouse.car_money,
            "ic"  : Crew.crew_summary,
            "isg" : Crew.stats_general,
            "isc" : Crew.stats_crime,
            "iss" : Crew.stats_shopping,
            "isb" : Crew.stats_banking,
            "isa" : Crew.stats_casino,
            "ist" : Crew.stats_territories,
            "isu" : Crew.stats_business,
            "ise" : Crew.stats_export,
            "ik"  : Crew.crew_skills,
            "rp"  : Recruit.recruit_peds,
            "ri"  : Recruit.intimidate_peds,
            "rb"  : Recruit.bribe_peds,
            "bw"  : Business.busy_withdraw,
            "bi"  : Business.busy_inspect,
            "bp"  : Business.busy_purchase,
            "bs"  : Business.busy_sell,
            "ms"  : Save.save_game,
            "ml"  : Save.load_game
        })

    def lose(self):
        answer = -1

        while answer == -1:
            system("cls")
            print("There's no more Crew Members backing you")
            print("\nThe Streets are full, but with the wrong guys")
            print("\nTime for you to go join them yourself.")

            print("\n\nAm I really not Mob Boss material?\n")
            print("1. Give me another chance, 10 more guys, no money needed. (Play Again)")
            print("2. Time to become a Pedestrian (Quit Game)")
        
            answer = input("\nYour response: ")
            answer = (-1 if answer == '' else answer)

        if answer == '1':
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
            print(f"\nThe {name}, is that right?")
            print("\nPress y to confirm. Hit enter to try again")
            sure = (True if input().lower() == 'y' else False)
            system("cls")
        
        return name

    # Returns True if new game
    def main_menu(self):
        render = PrettyTable()
        render.field_names = ["Key", "Option"]
        render.add_row(['n', "New Game"], divider=True)
        render.add_row(['l', "Load Game"], divider=True)
        render.add_row(['q', "Quit Game"], divider=True)

        choice = '?'

        while choice not in ('n', 'l', 'q'):
            system("cls")
            print(render)
            choice = input("\nChoose your path: ")
        
        if choice == 'n': return True
        elif choice == 'l':
            system("cls")
            success = load_game(self.world)

            if success: return False
            else: self.main_menu()
        else:
            system("cls")
            print("Thank you for playing Crime Book")
            exit()
    
    def offer_tutorial(self):
        answer = None

        while answer not in ('y', 'n'):
            system("cls")
            print("Would you like to play the tutorial?")
            answer = input("\ny or n: ").lower()
        
        if answer == 'y':
            tutorial = Tutorial()
            tutorial.play()



    # Main game loop
    def play(self):
        new = self.main_menu()

        if new:
            self.offer_tutorial()
            flush_input()
            self.world.player_gang_name = ("The " + self.get_gang_name())

            for city in self.world.cities.values():
                for block in city.blocks:
                    for gang in block.gangs:
                        if not gang.ai:
                            gang.name = self.world.player_gang_name
                            break

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
