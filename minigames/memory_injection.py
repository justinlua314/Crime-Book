from os import system

from random import randint as rand

from menu import input_buffer

class MemoryInjection:
    def __init__(self, length=5):
        self.length = length
        self.memory = []
        self.pointer = 0
        self.found = False

    def load(self):
        self.memory = []

        for _ in range(self.length):
            self.memory.append(rand(1, 9))
    
    def print_screen(self):
        print(' '.join([str(n) for n in self.memory]))
        print('^'.rjust(2 * self.pointer + 1))

    def lose(self):
        system("cls")
        self.print_screen()
        print("The Government has detected an intrusion! This can not be good...")
        self.found = True
        input("Press enter to continue")

    def interpret(self, code):
        for char in code:
            match(char):
                case '+':
                    self.memory[self.pointer] = min(self.memory[self.pointer] + 1, 255)
                
                case '-':
                    self.memory[self.pointer] -= 1
                    if self.memory[self.pointer] == 0: self.lose(); break
                
                case '>':
                    self.pointer = min(len(self.memory) - 1, self.pointer + 1)
                
                case '<':
                    self.pointer = max(self.pointer - 1, 0)
    
    def help(self):
        system("cls")
        self.print_screen()

        print("\nInject code to modify the memory")
        print("Sort the memory from lowest to highest -> left to right -> 1 2 3")

        tokens = {
            '>' : "Move memory pointer right",
            '<' : "Move memory pointer left",
            '+' : "Add 1 to memory address pointer is pointing at",
            '-' : "Subtracts 1 to memory address pointer is pointing at"
        }

        print("\nValid tokens:")

        for token,desc in tokens.items(): print(f"\t{token}\t{desc}")

        print("\nIf any memory cells hit 0, an alarm will be raised")

        input_buffer()

    
    def play(self):
        self.load()

        while self.memory == sorted(self.memory): self.load()
        attempts = 5

        while self.memory != sorted(self.memory) and attempts > 0:
            system("cls")
            print("You need to hack the memory. Type \"help\" for instructions\n")
            self.print_screen()
            print(f"Attempts left: {attempts}")

            code = input("Ijection code: ")

            if code.lower() == "help": self.help()
            else:
                self.interpret(code)
                if self.memory != sorted(self.memory): attempts -= 1

        if attempts == 0: self.lose()
        else: print("Hack succssful!")
        
        input_buffer()
        return self.found
