from os import system
from prettytable import PrettyTable
from random import randint as rand
from termcolor import colored
from time import sleep

from menu import valid_numeric_input, input_buffer

class RaceHorse:
    def __init__(self):
        self.position = 0
        self.targets = []
    
    def __repr__(self):
        pos = self.position
        return "<=]".rjust(pos, ' ').ljust(100 - pos - 3, ' ')

    def generate_targets(self, position_shifts, winner=False):
        self.targets = []
        pos = 0

        for _ in range(position_shifts):
            delta = rand(-20, 20)
            pos = min(max(pos + delta, 0), 96)
            self.targets.append(pos)
        
        if winner:
            for index in range(position_shifts - 1, 0, -1):
                threshold = (97 - (8 * (position_shifts - index - 1)))
                self.targets[index] = max(self.targets[index], threshold)
        else: self.targets[-1] = max(self.targets[-1], rand(80, 90))

    def think(self, target_index=0):
        target = self.targets[target_index]

        if self.position != target:
            self.position += (1 if target > self.position else -1)



def generic_roll(values):
    roll = rand(1, sum(values))
    sentinal = 0

    for index, pick in enumerate(values):
        sentinal += pick
        if roll <= sentinal: return index
    
    return -1

class HorseBetting:
    def __init__(self, pot=100):
        self.turns_per_race = 200
        self.money = pot
        self.start_money = pot
        self.bet_horse = 0
        self.bet_money = 0
        self.position_shifts = 20
        self.colors = ["red", "green", "blue", "magenta", "cyan"]
        self.horses = [RaceHorse() for _ in range(len(self.colors))]
        self.odds = [2 ** n for n in range(1, len(self.colors) + 1)]
        self.odds.reverse()
        self.barrier = ('-' * 103)

        self.wins = 0
        self.loses = 0
    
    def reset_race(self):
        for horse in self.horses:
            horse.position = 0
            horse.targets = []

    def draw_race(self):
        print(
            "Our Horse:", self.colors[self.bet_horse].capitalize(),
            "\tBet: $" + str(self.bet_money)
        )

        for index, horse in enumerate(self.horses):
            print(self.barrier)
            color = self.colors[index]
            print(colored(str(horse), color))

        print(self.barrier)

    def place_bets(self):
        render = PrettyTable()
        render.field_names = ["Horse #", "Color", "Odds"]
        render.add_row([0, "Leave Horse Racing", 0], divider=True)

        self.odds.reverse()

        for index in range(len(self.horses)):
            render.add_row(
                [index + 1, self.colors[index], "1/" + str(self.odds[index])],
                divider=True
            )
        
        self.odds.reverse()
        print(render)

        print(f"\nMoney: ${self.money}")

        selection = valid_numeric_input(
            "Which horse would you like to bet for", 0, len(self.horses), 0
        )

        if selection == 0:
            self.bet_money = 0
            return

        self.bet_horse = selection - 1

        bet = valid_numeric_input(
            "How much money would you like to bet? (0 to leave)", 0, self.money, (self.money // 2)
        )

        self.money -= bet
        self.bet_money = bet

    def finalize_game(self, winner):
        if self.bet_horse == winner:
            mult = self.odds[len(self.odds) - winner - 1]
            winnings = self.bet_money * mult

            print(f"\nCongrats! You won ${winnings}")
            self.money += winnings
            self.wins += 1
        else:
            print("\nYou lose, better luck next time!")
            self.loses += 1
        
        input_buffer()

    def play(self, world):
        while True:
            system("cls")
            self.place_bets()

            if self.bet_money == 0: break

            for countdown in range(3, 0, -1):
                system("cls")
                print(countdown)
                self.draw_race()
                sleep(1)
            
            winner = generic_roll(self.odds)

            for index, horse in enumerate(self.horses):
                horse.generate_targets(self.position_shifts, (index == winner))

            for turn in range(self.turns_per_race):
                target_index = int((self.position_shifts / self.turns_per_race) * turn)

                for horse in self.horses: horse.think(target_index)

                system("cls")
                self.draw_race()
                sleep(0.05)
            
            self.finalize_game(winner)
            world.think(False)

            if self.money == 0: break
            self.reset_race()
        
        system("cls")

        if self.money == 0: print("Oops! Your gambling pot is all empty!")

        print("Thanks for racing with us!\n\n")

        print("Wins:", self.wins, "\nLosses:", self.loses)

        try: print("Win/Loss Ratio:", round(self.wins / self.loses, 2))
        except: print("Win/Loss Ratio:", self.wins)

        print(f"\nTotal Winnings: ${self.money - self.start_money}")
        return self.money
