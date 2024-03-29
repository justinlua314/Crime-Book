from os import system
from prettytable import PrettyTable
from termcolor import colored

from cheats import cheat_codes

def input_buffer(): input("\n\nPress enter to continue")

# This function can be placed in Options as a placeholder to prevent crashes
# Example: Option("Manage Money Coffer", '', 'c', coming_soon)
def coming_soon(_):
    print("\nComing soon")
    input_buffer()

def valid_numeric_input(prompt="", min_value=0, max_value=1, default=0):
    choice = None

    while choice == None:
        choice = input(f"{prompt} (Default={default}) (Max={max_value}): ")

        if choice == '': return default

        if not choice.isnumeric():
            print("Choice must be a number\n")
            choice = None
            continue
        
        choice = int(choice)

        if choice < min_value or choice > max_value:
            print(f"Choice must be between {min_value} and {max_value}\n")
            choice = None

    return choice

def crew_count_input(ply, max_value=5000, safe=True):
    crew_count = len(ply.crew)
    print("\nCrew Members:", crew_count, '\n')
    maximum = min(crew_count - (1 if safe else 0), max_value)
    return valid_numeric_input("How many crew members do we send", 0, maximum, maximum)

def flush_input():
        try:
            import sys, termios
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        except ImportError:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()





class Option:
    def __init__(self, desc="", menu_id="", select='', func=None):
        self.description = desc
        self.menu_id = menu_id
        self.select = select
        self.trigger = (func if func != None else self.trigger)
    
    def __repr__(self):
        return ('_' + self.select + ". " + self.description)

    # Overwrite this function to do something else
    # and return to Main Menu
    def trigger(self, world): return self.menu_id



class Menu:
    def __init__(self, header="", choice_prompt="", options=[], main=False):
        self.header = header
        self.choice_prompt = choice_prompt
        self.options = options

        if main:
            last_option = Option("Quit Game", "exit", 'q')
        else:
            last_option = Option("Go Back", "back", 'z')

        self.options.append(last_option)
    
    def print_options(self):
        render = PrettyTable()
        render.field_names = ["Key", "Option"]

        for option in self.options:
            render.add_row(
                [option.select, option.description], divider=True
            )
        
        print(render)

    def prompt(self, world, shortcuts):
        valid_choices = [option.select for option in self.options]
        choice = None
        ply = world.player

        while choice not in valid_choices:
            system("cls")
            self.print_options()

            if world.cheated: print(colored("Cheated", "red"))

            pop = world.crew_population()

            if pop > 0: print(f"\nCrew Members: {len(ply.crew)} ({pop})")
            else: print("\nCrew Members:", len(ply.crew))
            
            print("Heat from Police:", ply.heat, '/', ply.heat_cap)

            if world.lawyers.count > 0:
                cost = world.lawyers.count * world.lawyers.cost
                print(f"Lawyers: {world.lawyers.count} (${cost})")

            if world.bank.savings == 0: print(f"${world.player.money}")
            else: print(f"${world.player.money} (${world.bank.savings})")

            if world.bank.loan > 0: print(f"Loan: ${world.bank.loan}")

            choice = input("\n\n" + self.choice_prompt + ": ").lower()
            system("cls")

            if ' ' in choice:
                tokens = choice.split(' ')

                if tokens[0] in shortcuts:
                    if tokens[1].isnumeric():
                        iters = min(int(tokens[1]) - 1, 50)

                        ply = world.player
                        before_heat = world.player.heat

                        for _ in range(iters):
                            shortcuts[tokens[0]](world)
                            flush_input()

                            if ply.heat >= ply.heat_cap or len(ply.crew) == 0:
                                break

                            world.think(before_heat != world.player.heat)
                        
                        world.think(before_heat != world.player.heat)


                    return shortcuts[tokens[0]](world)

            if choice in shortcuts: return shortcuts[choice](world)

            if choice in cheat_codes:
                cheat_codes[choice](world)
                world.cheated = True
                choice = None
                return

            flush_input()
        
        for option in self.options:
            if option.select == choice:
                return option.trigger(world)



class MenuManager:
    def __init__(self, main_menu="", menus={}, shortcuts={}):
        self.main_menu = main_menu
        self.active_menu = main_menu
        self.menus = menus          # menu_id : menu
        self.shortcuts = shortcuts  # key_combo : trigger
        self.menu_history = []

    # Returns two bools: (game_still_playing, world_should_think)
    def prompt(self, world):
        result = self.menus[self.active_menu].prompt(world, self.shortcuts)

        if result == "back":
            self.menu_history.pop()
            try: self.active_menu = self.menu_history[-1]
            except: self.active_menu = self.main_menu
        elif result == "exit": return False, False
        elif result != None:
            self.menu_history.append(result)
            self.active_menu = result
        else:
            self.menu_history = []
            self.active_menu = self.main_menu
            return True, True
        
        flush_input()
        return True, False
