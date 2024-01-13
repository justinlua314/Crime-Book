from os import system
from events import EventLog
from random import choice

from menu import valid_numeric_input, input_buffer

class Bank:
    def __init__(self):
        self.savings = 0
        self.savings_history = []

        self.save_withdraw_history = 0
        self.save_withdraw_limit = 1000
        self.save_withdraw_cap = 1000000
        self.save_withdraw_cooldown = 10
        self.save_withdraw_ticker = 0

        self.save_interest = 5
        self.dividend_cooldown = 10
        self.dividend_ticker = 0
        self.auto_withdraw = 0

        self.original_loan = 0
        self.loan = 0
        self.interest_rate = 5
        self.interest_cooldown = 30
        self.interest_ticker = 0

    def deposit_savings(self, world):
        print(f"Savings: ${self.savings}")
        ply = world.player
        print(f"Money: ${ply.money}\n")
        print("How much money would you like to deposit into your savings?")

        deposit = valid_numeric_input(
            "Deposit", 0, ply.money, ply.money // 2
        )

        if deposit == 0: return

        self.savings += deposit
        ply.money -= deposit

        print(f"Deposited ${deposit} into savings")
        limit_changed = False

        while self.save_withdraw_limit < self.savings and self.save_withdraw_limit < self.save_withdraw_cap:
            limit_changed = True
            self.save_withdraw_limit *= 10

        #self.save_withdraw_limit //= 10
        
        if limit_changed:
            print(f"\nSavings withdraw limit increased to ${self.save_withdraw_limit}")

        input_buffer()
    
    def withdraw_savings(self, world):
        limit = self.save_withdraw_limit - self.save_withdraw_history

        if limit == 0:
            print("You're pulling too much out of savings too quick. Let us gather some funds")
            input_buffer()
            return

        ply = world.player
        print(f"Savings: ${self.savings}")
        print(f"Withdraw Limit: ${limit}")
        print(f"Money: ${ply.money}\n")
        print("How much money would you like to withdraw from your savings?")

        withdraw = valid_numeric_input(
            "Withdraw", 0, min(limit, self.savings), 0
        )

        if withdraw == 0: return

        self.savings -= withdraw
        self.save_withdraw_history += withdraw
        ply.money += withdraw

        print(f"Withdrawn ${withdraw} from savings")
        input_buffer()


    def change_auto_withdraw(self, world):
        ply = world.player

        print(f"Money: ${ply.money}")
        print(f"Savings: ${self.savings}")
        print(f"Auto Withdraw: ${self.auto_withdraw}\n")

        print(f"Auto Withdraw allows you to pull money from your savings account automatically every {self.dividend_cooldown} turns")
        print("Money pulled this way is not counted towards your withdraw limit")

        print("\nHow much would you like to auto withdraw?")

        value = valid_numeric_input("Set Auto Withdraw", 0, 100000000, 0)

        self.auto_withdraw = value

        print(f"\nAuto Withdraw Account set to ${value}")
        input_buffer()

    def take_loan(self, world):
        from math import sqrt

        if self.original_loan != 0:
            print(f"You already have a loan for ${self.loan}")
            print("How's about we pay that off first?")
            input_buffer()
            return
        
        ply = world.player
        max_loan = (ply.money + self.savings) * int(sqrt(len(ply.crew)))
        print(f"It looks like you are elligable for a ${max_loan} loan")

        amount = valid_numeric_input(
            "What size of loan would you like to take out", 0, max_loan, 0
        )

        if amount == 0: return

        self.original_loan = amount
        self.loan = amount
        ply.money += amount

        print(f"\nYou are now locked into a ${amount} loan with a {self.interest_rate}% interest every {self.interest_cooldown} turns")
        input_buffer()
    
    def pay_loan(self, world):
        if self.loan == 0:
            print("You have no loan to pay off. Consider opening a line of credit today!")
            input_buffer()
            return

        ply = world.player
        print(f"Loan: ${self.loan}\nOriginal Loan: ${self.original_loan}")
        print(f"\nMoney: ${ply.money}")
        print("\nHow much money would you like to pay on your loan?")

        limit = min(ply.money, self.loan)
        payment = valid_numeric_input("Loan Request", 0, limit, limit)

        if payment == 0: return

        self.loan -= payment
        ply.money -= payment

        print(f"\nPaid ${payment} on your loan")

        if self.loan == 0:
            self.original_loan = 0
            print("Your loan is now paid off, feel free to open another line of credit any time")
        
        input_buffer()


    def sieze_property(self, world):
        log = EventLog()

        system("cls")
        print("You have fallen far too behind on your bank loan\n")
        print(f"Original Loan Amount: ${self.original_loan}")
        print(f"Current Loan Amount: ${self.loan}")
        print("\nYour property is being siezed to pay for your loan\n")

        if self.loan > self.savings:
            self.loan -= self.savings
            log.log("savings", "Money siezed from savings account", self.savings)
            self.savings = 0
        else:
            self.savings -= self.loan
            log.log("savings", "Money siezed from savings account", self.loan)
            self.loan = 0

        ply = world.player

        if self.loan > ply.money:
            self.loan -= ply.money
            log.log("wallet", "Money siezed from wallet", ply.money)
            ply.money = 0
        elif self.loan > 0:
            ply.money -= self.loan
            log.log("wallet", "Money siezed from wallet", self.loan)
            self.loan = 0
        
        if self.loan > world.gang_coffer:
            self.loan -= world.gang_coffer
            log.log("coffer", "Money siezed from Gang Coffer", world.gang_coffer)
            world.gang_coffer = 0
        elif self.loan > 0:
            world.gang_coffer -= self.loan
            log.log("wallet", "Money siezed from Gang Coffer", self.loan)
            self.loan = 0
        
        wh = world.warehouse
        cs = world.car_shop

        while self.loan > 0:
            if len(wh.items) > 0:
                # Getting random item from Warehouse.
                item_id = choice(list(wh.items.keys()))
                quality = choice(list(wh.items[item_id].keys()))
                item = wh.items[item_id][quality]
                value = (item.get_total_value() // 4)

                self.loan = max(self.loan - value, 0)
                log.log("warehouse", "Items siezed from Warehouse", item.count)
                wh.remove_item(item_id, quality, item.count)

            if self.loan == 0: break

            if len(cs.cars) > 0:
                item_id = choice(list(cs.cars.keys()))
                quality = choice(list(cs.cars[item_id].keys()))
                item = cs.cars[item_id][quality]
                value = (item.get_total_value() // 4)

                self.loan = max(self.loan - value, 0)
                log.log("carshop", "Cars siezed from Car Shop", item.count)
                cs.remove_car(item_id, quality, item.count)
            
            if len(wh.items) == 0 and len(cs.cars) == 0 and self.loan > 0:
                print("You are out of money and collateral. We will be back for more unless you pay up soon")
                break
        
        log.print_events()

        if self.loan > 0: print(f"\nLoan left after siezure: ${self.loan}")
        else:
            print("Your loan was paid off with siezed assets. Don't let it happen again")
            self.original_loan = 0

        input_buffer()



    def think(self, world):
        self.save_withdraw_ticker += 1

        if self.save_withdraw_ticker == self.save_withdraw_cooldown:
            self.save_withdraw_ticker = 0
            self.save_withdraw_history = 0
        
        self.savings_history.append(self.savings)
        self.dividend_ticker += 1

        if self.dividend_ticker == self.dividend_cooldown:
            self.dividend_ticker = 0
            dividend = int((sum(self.savings_history) // self.dividend_cooldown) * (self.save_interest / 100))
            #self.savings += dividend
            self.savings = min(self.savings + dividend, 20000000)
            self.savings_history = []

            if self.auto_withdraw > 0:
                amount = min(self.auto_withdraw, self.savings)
                self.savings -= amount
                world.player.money += amount
        
        if self.original_loan == 0: return

        self.interest_ticker += 1

        if self.interest_ticker == self.interest_cooldown:
            self.interest_ticker = 0
            self.loan += int(self.loan * (self.interest_rate / 100))

            if self.loan >= (self.original_loan * 2):
                self.sieze_property(world)
