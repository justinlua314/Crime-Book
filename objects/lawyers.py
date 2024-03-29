from menu import input_buffer

class Lawyers:
    def __init__(self):
        self.count = 0
        self.max_count = 500
        self.cost = 100
        self.effect = 1
        self.turns = 10
        self.turn_counter = 0
    
    def think(self, world):
        if self.count == 0: return

        ply = world.player
        reduction = (self.effect * self.count)
        ply.heat = max((ply.heat - reduction), 0)
        world.stats.add_stat("lawyer_heat", reduction)

        self.turn_counter += 1

        if self.turn_counter == self.turns:
            self.turn_counter = 0

            payment = (self.cost * self.count)
            lost = 0

            while self.count > 0 and payment > ply.money:
                self.count -= 1
                lost += 1
                payment -= self.cost
            
            if lost > 0:
                print("You lost", lost, "lawyers due to insufficient funds!")
                input_buffer()

            ply.money -= payment
