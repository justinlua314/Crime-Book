from os import system
from random import randint as rand

from menu import valid_numeric_input, input_buffer

class DoubleOrNothing:
    def __init__(self, money=100):
        self.money = money
        self.start_money = money
        self.bet = 0
        
        self.wins = 0
        self.loses = 0
        self.highest_multiplier = 1

    def play(self, world):
        while True:
            system("cls")
            if self.money == 0: break
            print(f"Money: ${self.money}")
            print("How much would you like to bet? (0 to stop playing)\n")
            self.bet = valid_numeric_input("Bet", 0, self.money, self.money // 2)

            if self.bet == 0: break

            world.stats.max_stat("largest_bet", self.bet)
            self.money -= self.bet
            multiplier = 1

            while True:
                system("cls")
                if multiplier > 1: print("Wager Doubled!\n")

                print(f"Original bet: ${self.bet}")
                print(f"Current wager: ${self.bet * multiplier}")
                print("\nDouble or Nothing?\n")

                print("1. Double")
                print("2. Keep Wager")
                choice = valid_numeric_input("Your choice", 1, 2, 1)

                if choice == 1:
                    if rand(1, 2) == 1: multiplier *= 2
                    else:
                        system("cls")
                        print("The wager has been lost!")
                        self.loses += 1
                        world.stats.max_stat("biggest_loss", self.bet)
                        input_buffer()
                        break
                else:
                    system("cls")
                    winnings = self.bet * multiplier
                    print(f"Congrats! You are walking away with ${winnings}")
                    self.money += winnings
                    self.wins += 1
                    self.highest_multiplier = max(self.highest_multiplier, multiplier)
                    world.stats.max_stat("biggest_win", winnings)
                    world.stats.max_stat("double_high", multiplier)
                    world.stats.inc_stat("double_won")
                    input_buffer()
                    break
            
            world.think(False)
        
        print("Wins:", self.wins, "\nLosses", self.loses)
        
        try: print("Win/Loss Ratio:", round(self.wins / self.loses), 2)
        except: print("Win/Loss Ratio:", self.wins)

        print(f"\nTotal Winnings: ${self.money - self.start_money}")
        return self.money
