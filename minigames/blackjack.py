from os import system
from prettytable import PrettyTable
from time import sleep

from menu import valid_numeric_input
from minigames.card_deck import CardDeck, CardHand

class BlackjackPlayer:
    def __init__(self, name="Unnamed", money=100):
        self.name = name
        self.money = money
        self.start_money = money
        self.bet = 0
        self.busted = False
        self.hand = CardHand()

        # Stats
        self.rounds_played = -1
        self.wins = 0
        self.loses = 0
        self.pushes = 0

    
    def __repr__(self): return self.hand.__repr__()
    def __len__(self): return len(self.hand)
    
    def new_hand(self, deck=CardDeck()):
        self.hand.flush()
        self.hand.draw(deck, 2)
        self.bet = 0
        self.busted = False
        self.rounds_played += 1

        return deck

    def score(self):
        value, aces = 0, 0

        for card in self.hand:
            if card.value == 1:     aces += 1
            elif card.value > 10:   value += 10
            else:                   value += card.value
        
        convert_aces = 0

        for card in self.hand:
            if card.value != 1: continue
            
            if value < 11: value += 11; convert_aces += 1
            else:
                value += 1

                if value > 21 and convert_aces > 0:
                    value -= 10
                    convert_aces -= 1
        
        return value

    def hand_row(self, most_cards=2):
        row = [self.name]
        for card in self.hand: row.append(card.value_name())

        if len(self.hand) < most_cards:
            row += [''] * (most_cards - len(self.hand))
        
        row.append(str(self.score()))
        return row

    def add_bet(self, value=0):
        self.money -= value
        self.bet += value

    def get_bet(self):
        if self.money == 0: return 0

        print("Please place your bet (0 to quit playing)")
        print(f"Money: ${self.money}")

        bet = valid_numeric_input("Bet", 0, self.money, (self.money // 2))
        self.add_bet(bet); return bet

    def turn(self, deck=CardDeck(), inspect=None):
        finished = False

        while not finished:
            print(f"\nBet: ${self.bet}")
            print("Select your play\n")
            total = self.score()

            if total == 21:
                print("Card Value 21, Standing")
                inspect()
                break

            print("1. Hit")
            print("2. Stand")

            can_double_down = (
                (len(self) == 2) and (self.money >= self.bet)
            )

            if can_double_down: print("3. Double Down")

            choices = (3 if can_double_down else 2)

            pick = valid_numeric_input(
                "\nYour Move: ", 1, choices
            )

            if pick < 1 or pick > choices:
                print("Invalid Choice\n"); pick = None; continue

            if pick == 1: # Hit
                self.hand.draw(deck)

                if self.score() > 21:
                    print("Busted!")
                    self.busted = True
                    finished = True
            elif pick == 2: finished = True; return # Stand
            elif pick == 3 and can_double_down: # Double down
                self.add_bet(self.bet)
                print("Bet increased to", self.bet)
                self.hand.draw(deck)

                if self.score() > 21:
                    print("Busted!")
                    self.busted = True

                finished = True

            inspect()
    
    def win(self):
        winnings = (self.bet * 2)
        print(f"You won ${self.bet}")
        self.money += winnings
        self.wins += 1
    
    def lose(self):
        print(f"You lost ${self.bet}")
        self.loses += 1

    def push(self):
        print("Push! Your bet has been returned to your wallet")
        self.money += self.bet
        self.pushes += 1

class BlackjackDealer(BlackjackPlayer):
    def __init__(self):
        super().__init__()
        self.name = ("(Dealer) " + self.name)
        self.hide_card = True
    
    def new_hand(self, deck=CardDeck()):
        self.hide_card = True
        return super().new_hand(deck)
    
    def hand_row(self, most_cards=2):
        row = [self.name]

        for index, card in enumerate(self.hand):
            if self.hide_card and index == 0: row.append('?')
            else: row.append(card.value_name())

        if len(self.hand) < most_cards:
            row += [''] * (most_cards - len(self.hand))

        if self.hide_card: row.append('?')
        else: row.append(str(self.score()))

        return row
    
    def turn(self, deck=CardDeck(), player=BlackjackPlayer(), inspect=None):
        self.hide_card = False
        inspect()

        if player.score() > 21: return

        while self.score() < 17:
            sleep(1)
            self.hand.draw(deck)
            inspect()

            if self.score() > 21:
                print("Dealer Busted!")

class Blackjack:
    def __init__(self, pot=0):
        self.dealer = BlackjackDealer()
        self.player = BlackjackPlayer("Player", pot)
        self.deck = CardDeck()
    
    def new_round(self):
        self.deck.reset(True)
        self.deck = self.dealer.new_hand(self.deck)
        self.deck = self.player.new_hand(self.deck)
    
    def inspect_table(self):
        headers = ["Name"]
        hands = [self.player, self.dealer]
        most_cards = len(max(hands, key=len))
        card_headers = ["Card " + str(x+1) for x in range(most_cards)]

        table = PrettyTable(headers + card_headers + ["Total"])
        print(self.dealer.hand)
        table.add_row(self.dealer.hand_row(most_cards))
        table.add_row(self.player.hand_row(most_cards))

        system("cls")
        print(table)
    
    def results(self):
        dealer_score = self.dealer.score()
        player_score = self.player.score()

        if (dealer_score > 21 and player_score < 22):
            self.player.win()
        elif not self.player.busted:
            if player_score > dealer_score:
                self.player.win()
            elif player_score == dealer_score:
                self.player.push()
            else:
                self.player.lose()
        else: self.player.lose()
    
    def play(self, world):
        while True:
            self.new_round()
            status = self.player.get_bet()

            if status == 0:
                system("cls")
                ply = self.player
                print("\n\nThank you for playing\n\n")

                print(
                    "Wins:", ply.wins, "\nLoses:", ply.loses,
                    "\nPushes:", ply.pushes
                )

                print(f"\nTotal Winnings: ${ply.money - ply.start_money}")

                try: print("Win/Loss Ratio:", round(ply.wins / ply.loses, 2))
                except: print("Win/Loss Ratio:", ply.wins)

                return ply.money

            self.inspect_table()
            self.player.turn(self.deck, self.inspect_table)
            self.dealer.turn(self.deck, self.player, self.inspect_table)

            sleep(1)
            self.results()

            print("\n\nNew Hand!\n\n")
            world.think(False)
