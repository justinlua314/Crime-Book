from os import system
from prettytable import PrettyTable

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
        choice = input(prompt + " (Default=" + str(default) + ") (Max=" + str(max_value) + "): ")

        if choice == '': return default

        if not choice.isnumeric():
            print("Choice must be a number\n")
            choice = None
            continue
        
        choice = int(choice)

        if choice < min_value or choice > max_value:
            print("Choice must be between", min_value, "and", max_value, '\n')
            choice = None

    return choice

def crew_count_input(ply, max_value=100000000):
    crew_count = len(ply.crew)
    print("\nCrew Members:", crew_count, '\n')
    maximum = min(crew_count - 1, max_value)
    return valid_numeric_input("How many crew members do we send", 0, maximum, maximum)





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

        while choice not in valid_choices:
            system("cls")
            ply = world.player

            self.print_options()
            print("\nCrew Members:", len(ply.crew))
            print("Heat from Police:", ply.heat, '/', ply.heat_cap)
            print('$', world.player.money, sep='')

            choice = input("\n\n" + self.choice_prompt + ": ")
            system("cls")

            if choice in shortcuts: return shortcuts[choice](world)

            if choice in cheat_codes:
                cheat_codes[choice](world)
                world.cheated = True
                choice = None
                return
        
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
        
        return True, False
