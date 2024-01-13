from time import sleep

class Heist:
    def __init__(self):
        self.crew = {}
        self.size = 1
    
    def tprint(self, message="\n"):
        print(message + "\n\n")
        sleep(5)
    
    def leave_fail(self): return

    def leave_win(self): return

    def lost(self, world):
        if len(self.crew) == 0:
            self.leave_fail(world)
            return True
        else: return False

    def next_member(self):
        if len(self.crew) == 0: return None
        else: return self.crew[list(self.crew)[0]]

    def fight_crowd(self, crowd, world, log):
        for target in crowd:
            while target.health > 0:
                member = self.next_member()
                if member == None: break
                member.fight(target, world, log, False)

                if member.health <= 0: self.crew.pop(id(member))
                if len(self.crew) == 0: break
        
        log.print_events()
        log.reset()
        return log

    def load_crew(self, world):
        ply = world.player
        if self.size > len(ply.crew): return

        scores = {} # crew_id : fitness score

        for id, member in ply.crew.items():
            scores[id] = (
                member.power_level() + sum([d[0] for d in member.stats.values()])
            )
        
        fitness = {} # crew_id : fitness score

        for id in sorted(scores, key=scores.get, reverse=True):
            fitness[id] = scores[id]
        
        ids = list(fitness)

        for _ in range(self.size):
            id = ids.pop(0)
            self.crew[id] = ply.crew.pop(id)
