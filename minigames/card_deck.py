from random import randint as rand
from random import choice, shuffle

class Card:
    def __init__(self, suite=0, value=0):
        self.suite = suite
        self.value = value
    
    def __repr__(self):
        if self.value == 0: return "Joker"
        return (self.value_name() + " of " + self.suite_name())

    def __add__(self, n): return (self.value + n)
    def __radd__(self, n): return self.__add__(n)
    def __sub__(self, n): return (self.value - n)

    def suite_name(self, suite=None):
        translate = ["Spades", "Clubs", "Hearts", "Diamonds"]

        if suite == None: return translate[self.suite]
        return translate[suite]
    
    def value_name(self, value=None):
        if value == None: value = self.value

        match value:
            case 0: return "Joker"
            case 1: return "Ace"
            case 11: return "Jack"
            case 12: return "Queen"
            case 13: return "King"
            case _: return str(value)
    
    def full_name(self): return self.__repr__()
    def random(self): return Card(rand(0, 3), rand(0, 13))


class CardDeck:
    def __init__(self, deck_count=1, jokers=False):
        self.deck_count = deck_count
        self.jokers = jokers
        self.cards = []
        start = (1 if jokers == False else 0)

        for _ in range(deck_count):
            for suite in range(0, 4):
                for value in range(start, 14):
                    self.cards.append(Card(suite, value))
    
    def __repr__(self):             return str(self.cards)
    def __getitem__(self, index):   return self.cards[index]
    def __iter__(self):             return iter(self.cards)
    def __len__(self):              return len(self.cards)
    
    def random(self, remove_card=False):
        if len(self.cards) == 0: return None
        card = choice(self.cards)
        if remove_card: self.cards.remove(card)
        return card
    
    def shuffle(self): shuffle(self.cards); return self
    def draw(self): return (None if len(self.cards) == 0 else self.cards.pop(0))

    def reset(self, shuffle=False):
        self.__init__(self.deck_count, self.jokers)
        if shuffle: self.shuffle()

class CardHand:
    def __init__(self):             self.cards = []
    def __getitem__(self, index):   return self.cards[index]
    def __len__(self):              return len(self.cards)
    
    def __repr__(self):
        hand = ""

        for index, card in enumerate(self.cards):
            hand += (str(index) + ": " + str(card) + '\n')
        
        return hand
    
    def recieve(self, card=Card()): self.cards.append(card)
    
    def draw(self, deck=CardDeck(), iter=1):
        for _ in range(iter): self.recieve(deck.draw())
    
    def play(self, index=0): return self.cards.pop(index)
    def flush(self): self.cards = []
