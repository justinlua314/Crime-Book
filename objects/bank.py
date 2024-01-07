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
        self.save_withdraw_cooldown = 10
        self.save_withdraw_ticker = 0

        self.save_interest = 5
        self.dividend_cooldown = 30
        self.dividend_ticker = 0

        self.original_loan = 0
        self.loan = 0
        self.interest_rate = 5
        self.interest_cooldown = 10
        self.interest_ticker = 0

    def deposit_savings(self, world):
        ply = world.player
        print("How much money would you like to deposit into your savings?")

        deposit = valid_numeric_input(
            "Deposit", 0, ply.money, ply.money // 2
        )

        if deposit == 0: return

        self.savings += deposit
        ply.money -= deposit

        print("Deposited $", deposit, " into savings", sep='')
        limit_changed = False

        while self.save_withdraw_limit < self.savings:
            limit_changed = True
            self.save_withdraw_limit *= 10
        
        if limit_changed:
            print("\nSavings withdraw limit increased to $", self.save_withdraw_limit, sep='')

        input_buffer()
    
    def withdraw_savings(self, world):
        limit = self.save_withdraw_limit - self.save_withdraw_history

        if limit == 0:
            print("You're pulling too much out of savings too quick. Let us gather some funds")
            input_buffer()
            return

        ply = world.player
        print("How much money would you like to withdraw from your savings?")

        withdraw = valid_numeric_input(
            "Withdraw", 0, min(limit, self.savings), 0
        )

        if withdraw == 0: return

        self.savings -= withdraw
        self.save_withdraw_history += withdraw
        ply.money += withdraw

        print("Withdrawn $", withdraw, " from savings", sep='')
        input_buffer()


    def take_loan(self, world):
        from math import sqrt

        if self.original_loan != 0:
            print("You already have a loan for $", self.loan, sep='')
            print("How's about we pay that off first?")
            input_buffer()
            return
        
        ply = world.player
        max_loan = (ply.money + self.savings) * int(sqrt(len(ply.crew)))
        print("It looks like you are elligable for a $", max_loan, " loan", sep='')

        amount = valid_numeric_input(
            "What size of loan would you like to take out", 0, max_loan, 0
        )

        if amount == 0: return

        self.original_loan = amount
        self.loan = amount
        ply.money += amount

        print("\nYou are now locked into a $", amount, " loan with a ", self.interest_rate, "% interest every ", self.interest_cooldown, " turns", sep='')
        input_buffer()
    
    def pay_loan(self, world):
        if self.loan == 0:
            print("You have no loan to pay off. Consider opening a line of credit today!")
            input_buffer()
            return

        ply = world.player
        print("Loan: $", self.loan, '\nOriginal Loan: $', self.original_loan, sep='')
        print("\nMoney: $", ply.money, sep='')
        print("\nHow much money would you like to pay on your loan?")

        limit = min(ply.money, self.loan)
        payment = valid_numeric_input("Loan Request", 0, limit, limit)

        if payment == 0: return

        self.loan -= payment
        ply.money -= payment

        print("\nPaid $", payment, " on your loan", sep='')

        if self.loan == 0:
            self.original_loan = 0
            print("Your loan is now paid off, feel free to open another line of credit any time")
        
        input_buffer()


    def sieze_property(self, world):
        log = EventLog()

        system("cls")
        print("You have fallen far too behind on your bank loan\n")
        print("Original Loan Amount: $", self.original_loan, sep='')
        print("Current Loan Amount: $", self.loan, sep='')
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

        if self.loan > 0: print("\nLoan left after siezure: $", self.loan, sep='')
        else:
            print("Your loan was paid off with siezed assets. Don't let it happen again")
            self.original_loan = 0

        input_buffer()



    def think(self, world):
        ply = world.player
        self.save_withdraw_ticker += 1

        if self.save_withdraw_ticker == self.save_withdraw_cooldown:
            self.save_withdraw_ticker = 0
            self.save_withdraw_history = 0
        
        self.savings_history.append(self.savings)
        self.dividend_ticker += 1

        if self.dividend_ticker == self.dividend_cooldown:
            self.dividend_ticker = 0
            dividend = sum(self.savings_history) // self.dividend_cooldown
            self.savings += dividend
            self.savings_history = []
        
        if self.original_loan == 0: return

        self.interest_ticker += 1

        if self.interest_ticker == self.interest_cooldown:
            self.interest_ticker = 0
            self.loan += int(self.loan * (self.interest_rate / 100))

            if self.loan >= (self.original_loan * 2):
                self.sieze_property(world)
