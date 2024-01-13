from random import randint as rand

from os import system
from random import choice

from events import EventLog
from menu import input_buffer
from heists.heist_base import Heist
from objects.humans import Cop, Criminal

class HeistPrison(Heist):
    def __init__(self):
        self.crew = {}
        self.size = 100
    
    # Lose 90% of crew members
    def leave_fail(self, world):
        system("cls")
        print("\nThe Breakout Crew is all dead!")
        input_buffer()

        system("cls")
        self.tprint("Wait.. Some of them survived!")
        self.tprint("And they ratted us out! Our HQ is getting raided right now!")

        ply = world.player
        stolen = int(len(ply.crew) * 0.9)

        for _ in range(stolen):
            if len(ply.crew) == 0: break
            ply.crew.pop(list(ply.crew)[0])
        
        self.tprint(f"{stolen} Crew Members got locked up, the rest of them managed to hide..")


        print("The Cops are gonna be watching us close. We better lay low for now")
        ply.heat = ply.heat_cap - int(ply.heat_cap * 0.9)
        input_buffer()

    
    def start(self, world):
        system("cls")
        self.tprint("We got charges on the side of the building. A Midnight Prison Break")
        log = EventLog()
        inmates = 0

        self.tprint("Boom! We're in the building. The prisoners are roaring and the guards are pissed!")

        self.tprint("Guards coming down the stairs! Take them out!")
            
        wave = [Cop(world) for _ in range(rand(4, 8))]
        log = self.fight_crowd(wave, world, log)

        if self.lost(world): return
        inmates += rand(100, 300)

        self.tprint("Some of the prisoners are fighting back! Take them out!")

        wave = [Criminal(world, choice(world.gang_names)) for _ in range(rand(2, 10))]
        log = self.fight_crowd(wave, world, log)

        if self.lost(world): return
        inmates += rand(150, 300)

        self.tprint("Police are already swarming that entrance we made. We need to find another way out")

        direction = rand(1, 3)

        if direction == 1:
            self.tprint("Get to the Mess Hall, take out any Guards who try to stop us!")
            self.tprint("Guards coming down the Hallway!")
            wave = [Cop(world) for _ in range(rand(4, 8))]
            log = self.fight_crowd(wave, world, log)
            if self.lost(world): return

            self.tprint("We've made it to the Mess Hall, now to find a safer exit...")
            self.tprint("SWAT Team! Repelling from the Ceilings take them out!!!")

            updates = [
                "That's the first wave, keep holding them off!",
                "Second wave clear, keep holding!",
                "Last wave clear, and the Prisoners found an exit. Let's get out of here!!"
            ]

            for text in updates:
                wave = [Cop(world) for _ in range(rand(4, 8))]
                for c in wave:
                    c.type = "Swat"
                    c.armor = 100
                    c.give_weapon(("shotgun" if rand(1, 3) == 1 else "pistol"), world)
            
            
                log = self.fight_crowd(wave, world, log)
                if self.lost(world): return

                inmates += rand(200, 500)
                self.tprint(text)

        elif direction == 2:
            self.tprint("We need to get to the Roof, our helicopters can shuttle these prisoners out")
            self.tprint("Start ascending up the stairs, fire down at those Cops trying to get in!")

            updates = [
                "First flight of stairs cleared, keep going!",
                "Another flight cleared, sounds like SWAT are breaching a different part of the Prison!",
                "Third flight cleared! Get to the roof quickly!"
            ]

            for text in updates:
                wave = [Cop(world) for _ in range(rand(3, 6))]
                log = self.fight_crowd(wave, world, log)
                if self.lost(world): return

                inmates += rand(200, 500)
                self.tprint(text)

            self.tprint("We've made it to the roof, but there's SWAT waiting for us! Take them out and jack the Helicopter!")

            
            wave = [Cop(world) for _ in range(rand(8, 12))]
            for c in wave:
                c.type = "Swat"
                c.armor = 100
                c.give_weapon(("shotgun" if rand(1, 3) == 1 else "pistol"), world)
            
            log = self.fight_crowd(wave, world, log)
            if self.lost(world): return
        else:
            self.tprint("Screw that, we're holding this Cell Block, the Cops can try and stop us")

            updates = [
                "Here comes the first wave, let's take them out!",
                "More police shuttling in the entrance",
                "Another wave down, how many of these guys are there?!",
                "I think we've almost cleared them!"
            ]

            for text in updates:
                wave = [Cop(world) for _ in range(rand(4, 8))]
                log = self.fight_crowd(wave, world, log)
                if self.lost(world): return

                inmates += rand(200, 500)
                self.tprint(text)

            self.tprint("Alright, the entrance looks clear, let's shuttle out!")
            self.tprint("Oh no! Swat guys right outside the entrance. Take them out this is the home stretch!")

            wave = [Cop(world) for _ in range(rand(4, 8))]
            for c in wave:
                c.type = "Swat"
                c.armor = 100
                c.give_weapon(("shotgun" if rand(1, 3) == 1 else "pistol"), world)
            
            log = self.fight_crowd(wave, world, log)
            if self.lost(world): return

            self.tprint("That's it! The Swat are out! I see our helicopters pulling in now, we're out of here!!")

        system("cls")
        self.tprint("\nYou did it! History has been made, the Prison has been opened! The masses are free")

        self.tprint("More importantly, they work for us now")

        log.log("crew", "Prisoners freed and recruited", inmates)
        world.player.give_random_crew_members(world, inmates)

        log.print_events()
        input_buffer()
        return self.crew
