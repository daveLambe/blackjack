from random import shuffle
# BlackJack Game


class Deck(object):
    """
    Class for a Deck of cards
    """


# Methods

    def __init__(self):
        values = range(2, 10) + ('Jack King Queen Ace').split()
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
    Class Object Attributes
    """


# Base Class - Player (Gambler & Dealer)

    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        self.current_hand = current_hand
        self.soft_hand_value = soft_hand_value
        self.hard_hand_value = hard_hand_value
        self.hit = hit
        self.stand = stand

# Methods

    def ask_hit(self):
        self.current_hand.append(DECK.deck_of_cards[0])
        DECK.remove_dealt_card()

    def print_current_hand_and_value(self):
        print 'Your current hand is:', ', '.join(self.current_hand)
        if self.soft_hand_value != self.hard_hand_value:
            print 'This hand has a Soft Value of', self.soft_hand_value, 'and a Hard Value of', self.hard_hand_value
        else:
            print 'This hand has a value of:', self.hard_hand_value

    def calc_hand_value(self):
        self.soft_hand_value = 0
        self.hard_hand_value = 0
        for i in range(len(self.current_hand)):
            if self.current_hand[i][0].isdigit():
                self.soft_hand_value += int(self.current_hand[i][0])
                self.hard_hand_value += int(self.current_hand[i][0])
            elif self.current_hand[i][0] == 'A':
                self.soft_hand_value += 1
                self.hard_hand_value += 11
            else:
                self.soft_hand_value += 10
                self.hard_hand_value += 10

    def check_win_hand(self):
        if self.soft_hand_value == 21 or self.hard_hand_value == 21:
            print 'Player has won!'
            return True
        elif self.soft_hand_value > 21 or self.hard_hand_value > 21:
            print 'Bust!'
            return True
        else:
            return False



class Gambler(Player):
    """
    Subclass - Gambler
    """
    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False, bet_amount=5, bankroll=100):
        Player.__init__(self, current_hand, soft_hand_value, hard_hand_value, hit, stand)
        self.bankroll = bankroll
        self.bet_amount = bet_amount


# Methods

    def print_bankroll(self):
        print 'Your bank contains', self.bankroll
        print
        print

    def add_bankroll(self, new_bankroll):
        self.bankroll += new_bankroll

    def change_bet_amount(self, new_bet_amount):
        self.bet_amount = new_bet_amount

    def player_turn(self):
        GAMBLER.print_current_hand_and_value()
        GAMBLER.print_bankroll()
        ask_player = raw_input('Hit or Stay?')
        if ask_player == 'hit':
            GAMBLER.ask_hit()
            GAMBLER.calc_hand_value()
            GAMBLER.print_current_hand_and_value()
        elif ask_player == 'stay':
            print 'You chose to stay'


class Dealer(Player):
    """
    Subclass - Dealer
    """
    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        Player.__init__(self, current_hand, soft_hand_value, hard_hand_value, hit, stand)


# Methods



# End Classes



# Start Logic

print "Let's play BlackJack!"

print 'Deck INFO'
DECK = Deck()
DECK.print_deck()
DECK.shuffle_deck()
print

print 'GAMBLER INFO'
GAMBLER = Gambler()
GAMBLER.ask_hit()
GAMBLER.ask_hit()
GAMBLER.print_current_hand_and_value()
GAMBLER.calc_hand_value()
GAMBLER.check_win_hand()
print

print 'DEALER INFO'
DEALER = Dealer()
DEALER.ask_hit()
DEALER.ask_hit()
GAMBLER.print_current_hand_and_value()
DEALER.check_win_hand()
print



print 'Logic printout:'

while not GAMBLER.check_win_hand():
    GAMBLER.player_turn()








# print
# print
# print 'Deck INFO'
# DECK = Deck()
# DECK.print_deck()
# DECK.shuffle_deck()
# print
# print
#
# print 'Gambler INFO'
# G = Gambler()
# G.add_bankroll(40)
# print G.bankroll
# G.ask_hit()
# G.ask_hit()
# DECK.print_deck()
# print G.current_hand
# G.calc_hand_value()
# print
# print
#
# print 'Dealer INFO'
# Dealy = Dealer()
# Dealy.ask_hit()
# Dealy.ask_hit()
# DECK.print_deck()
# print Dealy.current_hand
# Dealy.calc_hand_value()
