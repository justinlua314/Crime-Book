from random import randint as rand

from random import choice
from os import system

from events import EventLog
from menu import input_buffer
from heists.heist_base import Heist
from objects.humans import Ped, Cop, Criminal
from objects.warehouse import Item

class HeistBank(Heist):
    def __init__(self):
        self.crew = {}
        self.size = 50
    
    def leave_fail(self, world):
        system("cls")
        print("\nEveryone has died and the police are swarming the place!")
        input_buffer()

        system("cls")
        self.tprint("The Bank has discovered your account, everything has been zeroed out!")

        bank = world.bank

        bank.savings = 0
        bank.dividend_ticker = 0

        if bank.original_loan != 0:
            self.tprint(
                "They found out about your loan! They added a few zeros alright..."
            )

            bank.original_loan *= 20
            bank.loan = min(bank.loan * 20, bank.original_loan * 19)
        else:
            self.tprint(
                "Aww man they signed us in a loan contract! And didn't even fork over the money. Is that even legal?"
            )

            bank.original_loan = 2500000
            bank.loan = 2500000
        
        print("Now the cops are all over us and we owe the Bank in spades. What a bummer")
        world.player.heat = max(world.player.heat // 100, 20) ** 4
        input_buffer()

    def start(self, world):
        system("cls")
        self.tprint("Crew Members have entered the Bank and the mission has started")
        log = EventLog()

        wave = [Ped(world, (rand(1, 20) == 20)) for _ in range(rand(0, 5))]
        size = len(wave)

        if size > 0:
            self.tprint("We got some civilians playing hero!")
            log = self.fight_crowd(wave, world, log)
            
            if self.lost(world): return

            self.tprint("We took care of those crazies, moving to the Tellers")

        self.tprint("\"Give us the money, and let us into that vault now!!\"")

        if rand(1, 2) == 1:
            self.tprint("Security guards coming out! Take them down!")
            
            wave = [Cop(world) for _ in range(rand(1, 4))]
            for c in wave: c.type = "Security Guard"
            log = self.fight_crowd(wave, world, log)

        if self.lost(world): return
        
        self.tprint("We got the money from the Tills, now we hit the Vault!")
        self.tprint("Spoke too soon.. We got Cops coming in!")

        wave = [Cop(world) for _ in range(20)]
        log = self.fight_crowd(wave, world, log)
        if self.lost(world): return

        self.tprint("Finally we made it into the vault, team A bag the gold, team B, fend off the Cops!")

        wave = [Cop(world) for _ in range(rand(1, 10))]
        log = self.fight_crowd(wave, world, log)
        if self.lost(world): return

        self.tprint("Alright! We got the Gold and the Cash now let's get out of here!!")

        self.tprint("Clear those Cops at the exit and we're home free!")

        wave = [Cop(world) for _ in range(2 * rand(1, 2))]
        log = self.fight_crowd(wave, world, log)
        if self.lost(world): return

        self.tprint("We're out of the Bank, now let's get out of here!")

        if rand(1, 5000) == 3467:
            self.tprint("*Chopper Noises*")
            self.tprint("What is that? Are we not out yet?!")

            gang = choice(world.gang_names)

            self.tprint(f"Look in the sky! {gang} Gang coming down via chopper!")
            self.tprint("We have to pick them off or we lose the Gold")

            wave = [Criminal(world, gang) for _ in range(10)]
            for c in wave: c.arm(world)
            log = self.fight_crowd(wave, world, log)
            if self.lost(world): return

            self.tprint(f"We did it! Against all odds we took out the {gang}, the Bank, and the whole Police force!")
        
        system("cls")
        self.tprint("\nCongratulations, you have completed the Bank Heist")
        win_money = rand(100000, 500000)
        win_bars = rand(5, 20)

        log.log("money", "Money Stolen", win_money)
        log.log("gold", "Gold Bars Stolen", win_bars)

        world.player.money += win_money

        for _ in range(win_bars):
            world.warehouse.give_item(Item(
                "gold_bars", "Gold Bars", "household",
                8000, rand(5, 8), 1
            ))
        
        log.print_events()
        input_buffer()
        return self.crew
