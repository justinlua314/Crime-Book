from time import time
from prettytable import PrettyTable

from menu import input_buffer

class Statistic:
    def __init__(self, id, description, default_value=0):
        self.id = id
        self.description = description
        self.count = default_value
        self.starting = default_value
        self.money = False


class StatCounter:
    def __init__(self):
        self.start_time = time()

        self.data = {
            "General" : {
                "time_played" : Statistic(
                    "time_played", "Time played in hours"
                ),

                "turns_played" : Statistic(
                    "turns_played", "Turns played"
                ),

                "net_worth" : Statistic(
                    "net_worth", "Net Worth"
                ),

                "crew_recruited" : Statistic(
                    "crew_recruited", "Crew Members Recruited"
                ),

                "cheated" : Statistic(
                    "cheated", "Has Player cheated"
                ),

                "crew_died" : Statistic(
                    "crew_died", "Crew Members killed"
                ),

                "rations_eaten" : Statistic(
                    "rations_eaten", "Rations eaten by Crew Members"
                )
            },

            "Crime" : {
                "peds_robbed" : Statistic(
                    "peds_robbed", "Pedestrians Robbed"
                ),

                "cars_jacked" : Statistic(
                    "cars_jacked", "Cars Jacked"
                ),

                "houses_robbed" : Statistic(
                    "houses_robbed", "Houses Robbed"
                ),

                "computers_hacked" : Statistic(
                    "computers_hacked", "Government Computers Hacked"
                )
            },

            "Shopping" : {
                "gear_money" : Statistic(
                    "gear_money", "Money spent on Gear"
                ),

                "vests_purchased" : Statistic(
                    "vests_purchased", "Armor vests purchased"
                ),

                "bats_purchased" : Statistic(
                    "bats_purchased", "Baseball Bats purchased"
                ),

                "pistols_purchased" : Statistic(
                    "pistols_purchased", "Pistols purchased"
                ),

                "shotguns_purchased" : Statistic(
                    "shotguns_purchased", "Shutguns purchased"
                ),

                "rifles_purchased" : Statistic(
                    "rifles_purchased", "Rifles purchased"
                )
            },

            "Banking / Government" : {
                "savings_high" : Statistic(
                    "savings_high", "Savings account high score"
                ),

                "largest_loan" : Statistic(
                    "largest_loan", "Largest Loan paid off"
                ),

                "fed_money" : Statistic(
                    "fed_money", "Money donated to Feds"
                ),

                "heat_cap_high" : Statistic(
                    "heat_cap_high", "Highest Heat cap"
                ),

                "lawyer_heat" : Statistic(
                    "lawyer_heat", "Heat removed by Lawyers"
                ),

                "cities_purchased" : Statistic(
                    "cities_purchased", "Cities Purchased"
                )
            },

            "Casino" : {
                "winnings" : Statistic(
                    "winnings", "Winnings from gambling"
                ),

                "biggest_win" : Statistic(
                    "biggest_win", "Biggest gambling win"
                ),

                "biggest_loss" : Statistic(
                    "biggest_loss", "Biggest gambling loss"
                ),

                "largest_bet" : Statistic(
                    "largest_bet", "Largest bet"
                ),

                "bingo_won" : Statistic(
                    "bingo_won", "Bingo cards won"
                ),

                "blackjack_won" : Statistic(
                    "blackjack_won", "Hands of Blackjack won"
                ),

                "horse_won" : Statistic(
                    "horse_won", "Winning Horses betted on"
                ),

                "double_won" : Statistic(
                    "double_won", "Successful Double or Nothings"
                ),

                "wheel_won" : Statistic(
                    "wheel_won", "Winning spins on Wheel of Fortune"
                ),

                "fast_bingo" : Statistic(
                    "fast_bingo", "Fastest Bingo Win", 15
                ),

                "blackjack_hits" : Statistic(
                    "blackjack_hits", "Times hit in Blackjack"
                ),

                "double_downs" : Statistic(
                    "double_downs", "Times doubled down in Blackjack"
                ),

                "horse_high" : Statistic(
                    "horse_high", "Largest multiplier in Horse Racing"
                ),

                "double_high" : Statistic(
                    "double_high", "Highest Double or Nothing multiplier"
                ),

                "largest_fortune" : Statistic(
                    "largest_fortune", "Largest multiplier in Wheel of Fortune"
                )
            },

            "Territories" : {
                "crew_deployed" : Statistic(
                    "crew_deployed", "Crew members deployed"
                ),

                "blocks_controlled" : Statistic(
                    "blocks_controlled", "Blocks Controlled"
                ),

                "cities_controlled" : Statistic(
                    "cities_controlled", "Cities Controlled"
                ),

                "world_controlled" : Statistic(
                    "world_controlled", "Running the World"
                )
            },

            "Business" : {
                "scrapyard_owned" : Statistic(
                    "scrapyard_owned", "Scrapyards owned"
                ),

                "showroom_owned" : Statistic(
                    "car_showroom_owned", "Showrooms owned"
                ),

                "recruitment_owned" : Statistic(
                    "recruitment_owned", "Recruitment Offices owned"
                ),

                "grow_farm_owned" : Statistic(
                    "grow_farm_owned", "Grow Farms owned"
                ),

                "yayo_factory_owned" : Statistic(
                    "yayo_factory_owned", "Yayo Factories owned"
                ),

                "cars_sold" : Statistic(
                    "cars_sold", "Cars Sold"
                ),

                "smoke_grown" : Statistic(
                    "smoke_grown", "Smoke Packs grown"
                ),

                "yayo_made" : Statistic(
                    "yayo_made", "Yayo Packs manufactured"
                )
            }
        }

        # Formatting
        self.data["General"]["net_worth"].money = True
        self.data["Shopping"]["gear_money"].money = True
        self.data["Banking / Government"]["savings_high"].money = True
        self.data["Banking / Government"]["largest_loan"].money = True
        self.data["Banking / Government"]["fed_money"].money = True
        self.data["Casino"]["winnings"].money = True
        self.data["Casino"]["biggest_win"].money = True
        self.data["Casino"]["biggest_loss"].money = True
        self.data["Casino"]["largest_bet"].money = True

    def lookup_stat(self, id):
        for stat_data in self.data.values():
            for stat in stat_data.values():
                if stat.id == id: return stat
    
    def get_stat(self, id): return self.lookup_stat(id).count
    def set_stat(self, id, value): self.lookup_stat(id).count = value
    def add_stat(self, id, value): self.lookup_stat(id).count += value
    def inc_stat(self, id): self.lookup_stat(id).count += 1

    def min_stat(self, id, value):
        target = self.lookup_stat(id)
        target.count = min(target.count, value)

    def max_stat(self, id, value):
        target = self.lookup_stat(id)
        target.count = max(target.count, value)
    
    # Some stats should be refreshed only when looked at for performance reasons
    def refresh_stats(self, world):
        elapsed_time = round(((time() - self.start_time) / 60) / 60, 2)
        self.set_stat("time_played", elapsed_time)
        self.set_stat("net_worth", world.net_worth())
        self.set_stat("cheated", world.cheated)
        self.set_stat("crew_deployed", world.crew_population())

        city_control = 0
        block_control = 0
        world_control = True

        for city in world.cities.values():
            if city.top_gang() == world.player_gang_name:
                city_control += 1

            for block in city.blocks:
                if not block.controlling_gang().ai: block_control += 1
                else: world_control = False

        self.set_stat("blocks_controlled", block_control)
        self.set_stat("cities_controlled", city_control)
        self.set_stat("world_controlled", world_control)

        for id, business in world.business.locations.items():
            self.set_stat(f"{id}_owned", business.count)
    
    def export_stats(self, world):
        self.refresh_stats(world)
        export_data = "Crime Game Statistics\n"
        export_data += (f"Players Gang: {world.player_gang_name}\n\n")
        render = PrettyTable()
        render.field_names = ["Statistic", "Value"]

        for category, data in self.data.items():
            export_data += f"{category}\n"

            for stat in data.values():
                value = stat.count
                if stat.money: value = (f"${value}")
                render.add_row([stat.description, value], divider=True)
            
            export_data += (str(render) + "\n\n")
            render.clear_rows()

        with open("Game Statistics.txt", 'w') as f:
            f.write(export_data)
            f.close()
        
        print("Game statistics exported to \"Game Statistics.txt\"")
        input_buffer()
