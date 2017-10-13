from random import shuffle
# BlackJack Game


class Deck(object):
    """
    Class for a Deck of cards
    """
    def __init__(self):
        values = range(2, 11) + ('Jack King Queen Ace').split()
        suits = 'Diamonds Clubs Spades Hearts'.split()
        self.deck_of_cards = ['%s of %s' % (v, s) for v in values for s in suits]

    def print_deck(self):
        print self.deck_of_cards
        print len(self.deck_of_cards)

    def shuffle_deck(self):
        shuffle(self.deck_of_cards)
        print self.deck_of_cards

    def deal_card(self):
        return self.deck_of_cards[0]

    def remove_dealt_card(self):
        del self.deck_of_cards[0]


class Player(object):
    """
    Base Class - Player (Gambler & Dealer)
    """
    def __init__(self, current_hand=[], hand_value=0, hit=False, stand=False):
        self.current_hand = current_hand
        self.hand_value = hand_value
        self.hit = hit
        self.stand = stand

    def ask_hit(self):
        self.current_hand.append(DECK.deck_of_cards[0])
        print self.current_hand
        DECK.remove_dealt_card()


# CURRENTLY WORKING ON THIS

    def calc_hand_value(self):
        for i in range(len(self.current_hand)):
            print self.current_hand[i]
            self.hand_value = self.current_hand[i][0]
            print self.hand_value


class Gambler(Player):
    """
    Subclass - Gambler
    """
    def __init__(self, current_hand=[], hand_value=0, hit=False, stand=False, bet_amount=5, bankroll=100):
        Player.__init__(self, current_hand, hand_value, hit, stand)
        self.bankroll = bankroll
        self.bet_amount = bet_amount

    def add_bankroll(self, new_bankroll):
        self.bankroll += new_bankroll

    def change_bet_amount(self, new_bet_amount):
        self.bet_amount = new_bet_amount

class Dealer(Player):
    """
    Subclass - Dealer
    """
    def __init__(self, current_hand=[], hand_value=0, hit=False, stand=False):
        Player.__init__(self, current_hand, hand_value, hit, stand)

print 'Deck INFO'
DECK = Deck()
DECK.print_deck()
DECK.shuffle_deck()
print
print

print 'Gambler INFO'
P = Gambler()
P.add_bankroll(40)
print P.bankroll
P.ask_hit()
P.ask_hit()
DECK.print_deck()
print
print
print 'Dealer INFO'
Dealy = Dealer()
Dealy.ask_hit()
Dealy.ask_hit()
DECK.print_deck()

P.calc_hand_value()


