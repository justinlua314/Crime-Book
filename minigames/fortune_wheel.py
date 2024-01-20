from random import shuffle
from time import sleep
from os import system

from menu import valid_numeric_input, input_buffer


class FortuneWheel:
    def __init__(self, money=100):
        self.tokens = { # multiplier : odds
            0 : 40,
            2 : 25,
            5 : 15,
            10 : 8,
            20 : 6,
            40 : 5,
            100 : 1
        }

        self.slots = []
        self.shuffle()
        self.pointer = 0
        self.screen_size = 11
        self.spin_iters = 80
        self.friction = 0.002

        self.money = money
        self.start_money = money
        self.bet = 0
        
        self.wins = 0
        self.losses = 0
    
    def shuffle(self):
        self.slots = []
        for key in self.tokens: self.slots += ([key] * self.tokens[key])
        shuffle(self.slots)
    
    def print_screen(self):
        index = self.pointer - (self.screen_size // 2) + 1
        if index < 0: index = (len(self.slots) + index - 1)

        render = ""

        for _ in range(self.screen_size):
            mult = self.slots[index]

            if mult < 10: render += "  "
            elif mult < 100: render += ' '
            
            render += f"{self.slots[index]} "

            index += 1
            if index == len(self.slots): index = 0
        
        print(render[:-1])
        print('^'.rjust((self.screen_size // 2) * 4 + 3))

    def spin(self):
        iters = self.spin_iters
        speed = self.friction

        for _ in range(iters):
            system("cls")
            self.print_screen()
            self.pointer += 1
            if self.pointer == len(self.slots): self.pointer = 0

            sleep(speed)
            speed += self.friction
        
        return self.slots[self.pointer]
    
    def play(self, world):
        while True:
            if self.money == 0: break
            system("cls")
            self.print_screen()

            print(f"\nMoney: ${self.money}")
            print("How much would you like to bet? (0 to stop playing)\n")
            self.bet = valid_numeric_input("Bet", 0, self.money, self.money // 2)

            if self.bet == 0: break
            self.money -= self.bet
            world.stats.max_stat("largest_bet", self.bet)

            self.shuffle()
            mult = self.spin()

            if mult == 0:
                print("Too bad, better luck on the next spin")
                self.losses += 1
                world.stats.max_stat("biggest_loss", self.bet)
            else:
                winnings = (self.bet * mult)
                print(f"Congrats! You won ${winnings} on a x{mult} multiplier!")
                self.money += winnings
                self.wins += 1
                world.stats.max_stat("largest_fortune", mult)
                world.stats.max_stat("biggest_win", winnings)
                world.stats.inc_stat("wheel_won")
            
            world.think(False)
            input_buffer()
        
        print("\nWins:", self.wins, "\nLosses", self.losses)
        
        try: print("Win/Loss Ratio:", round(self.wins / self.losses), 2)
        except: print("Win/Loss Ratio:", self.wins)

        print(f"\nTotal Winnings: ${self.money - self.start_money}")
        return self.money
