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
        print self.__class__.__name__, 'current hand is:', ', '.join(self.current_hand)
        if self.soft_hand_value != self.hard_hand_value:
            print self.__class__.__name__, 'hand has a Soft Value of', self.soft_hand_value, 'and a Hard Value of', self.hard_hand_value
        else:
            print self.__class__.__name__, 'hand has a value of:', self.hard_hand_value

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

    def check_win_or_bust(self):
        if self.soft_hand_value == 21 or self.hard_hand_value == 21:
            print self.__class__.__name__, 'has won!'
            return True
        # elif self.soft_hand_value > 21 or self.hard_hand_value > 21:
        #     print self.__class__.__name__, 'has bust!'
        #     return True
        else:
            return False

    def check_bust(self):
        if self.soft_hand_value > 21 or self.hard_hand_value > 21:
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

    def gambler_turn(self):
        GAMBLER.print_current_hand_and_value()
        GAMBLER.print_bankroll()
        ask_player = raw_input('Hit or Stay?')
        if ask_player == 'hit':
            GAMBLER.ask_hit()
            GAMBLER.calc_hand_value()
            GAMBLER.print_current_hand_and_value()
        elif ask_player == 'stay':
            print 'Dealers turn'
            DEALER.dealer_turn()


class Dealer(Player):
    """
    Subclass - Dealer
    """
    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        Player.__init__(self, current_hand, soft_hand_value, hard_hand_value, hit, stand)


# Methods

    def dealer_turn(self):
        while DEALER.soft_hand_value < 17 and DEALER.hard_hand_value < 17:
            DEALER.ask_hit()
            DEALER.calc_hand_value()
            DEALER.print_current_hand_and_value()
            DEALER.check_win_or_bust()
        print 'At least 17 reached'



# End Classes



# Start Logic
print
print
print "Let's play BlackJack!"
print
print


# SUDO CODE!
# Make a Deck
game_over = False
DECK = Deck()
# Shuffle deck
DECK.shuffle_deck()
# make a gambler
GAMBLER = Gambler()
# make a dealer
DEALER = Dealer()
# give gambler two cards
GAMBLER.ask_hit()
GAMBLER.ask_hit()
# give dealer two cards
DEALER.ask_hit()
DEALER.ask_hit()
# calc gambler hand and value
GAMBLER.calc_hand_value()
# print gambler hand and value
GAMBLER.print_current_hand_and_value()
print
print
# calc dealer hand and value
DEALER.calc_hand_value()
# print dealers hand and value
DEALER.print_current_hand_and_value()
print
print
# check if gambler wins already
GAMBLER.check_win_or_bust()
# check if dealer wins already
DEALER.check_win_or_bust()


while not GAMBLER.check_win_or_bust() or DEALER.check_win_or_bust():
    GAMBLER.gambler_turn()

# If not, gambler can hit or stay
# if hit:
#     give new card
#     see if they win or bust
#     continue
# if stay:
#     give dealer cards until at least 17
#     see if dealer bust or win
#     if not bust or 21:
#         check if dealer or player higher


# print 'Deck INFO'
# DECK = Deck()
# DECK.print_deck()
# DECK.shuffle_deck()
# print

# print 'GAMBLER INFO'
# GAMBLER = Gambler()
# GAMBLER.ask_hit()
# GAMBLER.ask_hit()
# GAMBLER.print_current_hand_and_value()
# GAMBLER.calc_hand_value()
# GAMBLER.check_win_or_bust()


# print 'DEALER INFO'
# DEALER = Dealer()
# DEALER.ask_hit()
# DEALER.ask_hit()
# DEALER.print_current_hand_and_value()
# DEALER.check_win_or_bust()



# print 'Logic printout:'

# while not GAMBLER.check_win_or_bust():
#     GAMBLER.player_turn()









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
