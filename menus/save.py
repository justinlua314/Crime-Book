import os, pickle

from prettytable import PrettyTable

from menu import Menu, Option, input_buffer, valid_numeric_input

def verify_save_folder():
    if not os.path.exists("saves"):
        os.makedirs("saves")

def print_saves():
    verify_save_folder()

    render = PrettyTable()
    render.field_names = ["Key", "Save Slot"]
    render.add_row([0, "Cancel Selection"], divider=True)

    for i in range(1, 11):
        if os.path.isfile(f"saves/save{i}"):
            try:
                data = pickle.load(open(f"saves/save{i}", "rb"))
                name = data.player_gang_name
                played = data.stats.data["General"]["time_played"].count
                
                render.add_row([i, f"{name} : {played}"], divider=True)
            except:
                render.add_row([i, "Corrupt save file"], divider=True)
        else:
            render.add_row([i, "Empty"], divider=True)
    
    print(render)

def save_game(world):
    print_saves()

    selection = valid_numeric_input("Select a save slot", 0, 10, 0)
    if selection == 0: return

    try:
        save = open(f"saves/save{selection}", "wb")

        pickle.dump(world, save)
        save.close()

        print(f"\nGame saved successfully to slot {selection}")
    except:
        print("\nSomething went wrong while saving :(")
    
    input_buffer()

# Returns True if save was loaded successfully
def load_game(world):
    print_saves()

    selection = valid_numeric_input("Select a save slot", 0, 10, 0)
    if selection == 0: return False

    if not os.path.isfile(f"saves/save{selection}"):
        print("\nCannot load empty save file")
        input_buffer()
        return False

    try:
        load = open(f"saves/save{selection}", "rb")
        new_world = pickle.load(load)

        load.close()

        if type(new_world) != type(world):
            print(f"\nCould not load save{selection}. World corrupted")
            input_buffer()
            return False

        world.__dict__ = new_world.__dict__.copy()

        print(f"\nsave{selection} loaded successfully!")
    except:
        print(f"\nSomething went wrong while attempting to load save{selection}")
        return False
    
    input_buffer()
    return True

menu_save = Menu(
    "Manage save game", "What would you like to do", [
        Option("Save Game", '', 's', save_game),
        Option("Load Game", '', 'l', load_game)
    ]
)
