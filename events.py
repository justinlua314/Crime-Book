from prettytable import PrettyTable

class Event:
    def __init__(self, id="", description="", count=1):
        self.id = id
        self.description = description
        self.count = count
    
    def __repr__(self): return (self.description + ": " + str(self.count))
    def log(self, count=1): self.count += count



class EventLog:
    def __init__(self):
        self.events = {} # event.id : event
    
    def __repr__(self):
        message = "\nEvent Log:\n"

        for _,event in self.events.items():
            message += (str(event) + '\n')

        return message
    
    def print_events(self):
        if len(self.events) == 0: return

        print("\nEvent Log:\n")
        render = PrettyTable()
        render.field_names = ["Event", "Count"]

        for _,event in self.events.items():
            render.add_row([event.description, event.count], divider=True)
        
        print(render)

    def get_count(self, id=""):
        if self.id in self.events.keys(): return self.events[id].count
        else: return 0

    def search_count(self, search=""):
        total = 0

        for id, event in self.events.items():
            if search in id or search in event.description:
                total += event.count
        
        return total

    def log(self, id="", description="", count=1):
        if id in self.events.keys(): self.events[id].log(count)
        else: self.events[id] = Event(id, description, count)
    
    def reset(self): self.events = {}
