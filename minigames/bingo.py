from os import system
from random import choice, sample
from time import sleep
from termcolor import colored

from menu import valid_numeric_input, input_buffer

class Bingo:
    def __init__(self, money=100):
        self.money = money
        self.start_money = money
        self.bet = 0
        self.turns = 14
        self.ball_count = 28
        self.turns_left = self.turns
        self.balls = []
        self.board = [[0] * 5 for _ in range(5)]

        self.wins = 0
        self.loses = 0
    
    def __repr__(self):
        render = ""

        for row in self.board:
            for cell in row:
                if cell == 'X': render += 'X'
                elif cell < 10: render += '0'
                render += str(cell) + "  "
            render += "\n\n"
        
        return render
    
    def draw_board(self):
        for row in self.board:
            for cell in row:
                if cell =='X': print(colored("XX ", "cyan"), end='')
                elif cell < 10: print(f"0{cell} ", end='')
                else: print(f"{cell} ", end='')
                print("  ", end='')

            print('\n')

    def randomize_board(self):
        picks = sample(self.balls, 25)

        for row in range(5):
            for cell in range(5):
                pick = choice(picks)
                picks.remove(pick)
                self.board[row][cell] = pick
        
        self.board[2][2] = 'X'
    
    def reset(self):
        self.balls = [n for n in range(1, self.ball_count + 1)]
        self.turns_left = self.turns
        self.randomize_board()

    def mark(self, pick):
        marked = False

        for row in range(5):
            for cell in range(5):
                if self.board[row][cell] == pick:
                    self.board[row][cell] = 'X'
                    marked = True
                    break
            
            if marked == True: break

    def turn(self):
        pick = choice(self.balls)
        self.balls.remove(pick)
        self.mark(pick)
        print(f"{pick}!\n")
        print(self)

    def check_win(self):
        for row in self.board:
            if len(set(row)) <= 1: return True

        for column in range(5):
            col = [self.board[i][column] for i in range(5)]
            if len(set(col)) <= 1: return True
        
        diag = [self.board[i][i] for i in range(5)]
        if len(set(diag)) <= 1: return True

        diag = [self.board[4 - i][i] for i in range(5)]
        if len(set(diag)) <= 1: return True

        return False

    def commentate(self, message=''):
        system("cls")
        print(message, '\n')
        self.draw_board()
        sleep(1.5)

    def play(self, world):
        while self.money > 0:
            system("cls")
            print("Bet $0 to quit playing")
            bet = valid_numeric_input(
                "How much would you like to bet", 0, self.money, self.money // 2
            )

            if bet == 0: break

            self.bet = bet
            self.money -= bet
            self.reset()

            while self.turns_left > 0:
                pick = choice(self.balls)
                self.balls.remove(pick)

                self.commentate(str(pick) + '!')

                self.mark(pick)
                self.commentate()

                if self.check_win():
                    shout = "Bingo!"
                    speed = (self.turns - self.turns_left)

                    if speed < 7:
                        shout += " You also earned a x"
                        match(speed):
                            case 4: shout += "16"; self.bet *= 8
                            case 5: shout += "8"; self.bet *= 4
                            case 6: shout += "4"; self.bet *= 2
                        
                        shout += " speed bonus!"

                    self.commentate(shout)
                    winnings = self.bet * 2
                    self.money += winnings
                    self.wins += 1

                    print(f"\nYou won ${winnings}")
                    input_buffer()
                    break
                else:
                    self.turns_left -= 1
            
            world.think(False)
            
            if self.turns_left == 0:
                print("\nUnlucky, no winnings for you")
                self.loses += 1
                input_buffer()

        system("cls")
        print("\n\nThank you for playing\n\n")

        print("Wins:", self.wins, "\nLoses:", self.loses)

        print(f"\nTotal Winnings: ${self.money - self.start_money}\n")

        try: print("Win/Loss Ratio:", round(self.wins / self.loses, 2))
        except: print("Win/Loss Ratio:", self.wins)

        return self.money
