from os import system
from time import sleep

from random import randint as rand

from menu import Menu, Option, input_buffer, flush_input

class SimpleMenu(Menu):
    def __init__(self, header="", choice_prompt="", options=[]):
        self.header = header
        self.choice_prompt = choice_prompt
        self.options = options
    
    def prompt(self):
        valid_choices = [option.select for option in self.options]
        choice = None

        while choice not in valid_choices:
            system("cls")
            self.print_options()

            choice = input("\n\n" + self.choice_prompt + ": ").lower()
            system("cls")

        for option in self.options:
            if option.select == choice:
                return option.trigger(None)

def recruit_peds(_):
    print("Congrats! You recruited pedestrians!")
    input_buffer()

menu_recruit = SimpleMenu(
    "Recruit Menu", "Press p and hit enter to recruit pedestrians", [
        Option("Recruit Pedestrians", '', 'p', recruit_peds)
    ]
)

menu_home = SimpleMenu(
    "Tutorial", "Press r and hit enter to go to the recruit menu", [
        Option("Recruit new Members", "menu_recruit", 'r')
    ]
)

class Tutorial:
    def __init__(self):
        self.crew = 0

    def play(self):
        system("cls")
        
        intro = """Welcome to Crime Game
This game is about getting loot, collecting money, and controlling the world.

You navigate menus by typing their keys, and hitting enter.
Try entering the letter 'r' to enter the recruitment menu on the next screen."""

        print(intro)
        input_buffer()

        print("Crew Members: 0")
        menu_home.prompt()
        system("cls")
        menu_recruit.prompt()
        system("cls")
        print("Great work! Pedestrians have been recruited and 1 turn has passed in game.")
        flush_input()
        sleep(3)
        print("But all that typing is tedious, and we need a lot of guys.")
        sleep(4)
        print("\nLet's see, we typed r for recruitment, then p for pedestrians")
        sleep(4)
        print("\nTry typing 'rp' in the next screen and hit enter to skip a menu")
        self.crew += rand(3, 12)

        input_buffer()

        check = ""

        while check != "rp":
            if (' ' in check and check.split(' ')[0] == "rp"): break
            system("cls")
            print(f"Crew Members: {self.crew}")
            menu_home.print_options()

            check = input(
                "Enter rp to recruit Pedestrians faster: "
            ).lower()
        
        system("cls")
        recruit_peds(None)
        self.crew += rand(3, 12)
        system("cls")
        print("\nVery great work. Last tip then we can get on with the fun")
        sleep(3)
        print("\n'rp' is a macro, and there are many macros in the game")
        sleep(3)
        print("\nMacros can be ran multiple times by adding a number after the macro")
        sleep(4)

        print("\nFor example: rp 10")
        print("\tThis recruits Pedestrians 10 times")

        sleep(4)
        print("\nMacro combos are limited to 50 iterations")
        print("Try using a macro in the next screen")

        flush_input()
        input_buffer()

        check = ""

        while True:
            system("cls")
            print(f"Crew Members: {self.crew}")
            menu_home.print_options()

            check = input("Type rp followed by a number (rp 10): ").lower()

            if ' ' in check:
                tokens = check.split(' ')

                if tokens[0] != "rp": continue
                if not tokens[1].isnumeric(): continue

                iters = int(tokens[1])

                if iters < 1 or iters > 50:
                    print("\nMacro iterations must be between 1 and 50")
                    input_buffer()
                    continue
                
                print(f"\nWe are ready to recruit Pedestrians {iters} times\nHold the enter key to rapidly recruit")

                input_buffer()
                system("cls")

                for _ in range(iters):
                    recruit_peds(None)
                    self.crew += rand(3, 12)

                break
        
        system("cls")
        print("That's all for this Tutorial. Have fun and explore around!")
        sleep(4)
        flush_input()
        input_buffer()
