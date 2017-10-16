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
    Class for Player (Gambler or Dealer)
    Has attributes and methods used by both
    """


# Base Class - Player (Gambler & Dealer)

    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        self.current_hand = current_hand
        self.soft_hand_value = soft_hand_value
        self.hard_hand_value = hard_hand_value
        self.hit = hit
        self.stand = stand

# Methods

    def deal_card(self):
        self.current_hand.append(DECK.deck_of_cards[0])
        DECK.remove_dealt_card()

    def print_current_hand_and_value(self):
        self.calc_hand_value()
        print self.__class__.__name__, 'hand contains:', ', '.join(self.current_hand)
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

    def check_win(self):
        # Sudo hard vs soft
        # if players hard hand value is greater than 21
        #     players hard hand value = players soft hand value
        global game_over
        if self.soft_hand_value == 21 or self.hard_hand_value == 21:
            print self.__class__.__name__, 'has won! - from check win'
            game_over = True
            return True
        else:
            return False

    def check_bust(self):
        global game_over
        if self.soft_hand_value > 21:
            print self.__class__.__name__, 'is bust! - from check bust'
            game_over = True
            return True
        else:
            return False

    def check_use_hard_or_soft(self):
        global winner
        print
        if self.soft_hand_value != self.hard_hand_value:
            if self.hard_hand_value < 21:
                self.soft_hand_value = self.hard_hand_value
            else:
                print 'Hard value too high to use'

    def check_winning_hand(self, a, b):
        global winner
        print
        print 'Final score.. \nDealer: %s \nGambler: %s' % (b.soft_hand_value, a.soft_hand_value)
        if a.soft_hand_value == b.soft_hand_value:
            print 'Tied hand!'
            winner = 'Nobody!'
        elif a.soft_hand_value > b.soft_hand_value:
            print 'Gambler wins by Higher Valued hand!'
            winner = 'Gambler'
        else:
            print 'Dealer wins by Higher Valued hand!'
            winner = 'Dealer'


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
        global gambler_turn_over
        # GAMBLER.print_bankroll()
        print
        ask_player = raw_input('Hit or Stay?')
        if ask_player == 'hit':
            self.deal_card()
            self.print_current_hand_and_value()
            return True
        elif ask_player == 'stay':
            print 'Here is the final Gambler hand...'
            self.print_current_hand_and_value()
            gambler_turn_over = True
            return False


class Dealer(Player):
    """
    Subclass - Dealer
    """
    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        Player.__init__(self, current_hand, soft_hand_value, hard_hand_value, hit, stand)


# Methods

    def dealer_turn(self):
        global game_over
        global dealer_turn_over
        print '\nDealers turn..'
        if self.hard_hand_value < 21:
            if self.hard_hand_value < 17:
                'Dealer needs to draw a card'
                self.deal_card()
                DEALER.print_current_hand_and_value()
                return True
            else:
                print 'Dealer does not need to draw a card'
                dealer_turn_over = True
                return False
        elif self.soft_hand_value < 17:
            print 'Dealer needs to draw a card'
            self.deal_card()
            DEALER.print_current_hand_and_value()
            return True
        else:
            print 'Dealer does not need to draw a card'
            dealer_turn_over = True
            return False


# End Classes

# Sudo Main logic - Start Game

print
print
print "Let's play BlackJack!"
print
print
game_over = False
gambler_turn_over = False
dealer_turn_over = False
winner = 'blank'
DECK = Deck()
DECK.shuffle_deck()
GAMBLER = Gambler()
GAMBLER.deal_card()
GAMBLER.deal_card()
DEALER = Dealer()
DEALER.deal_card()
DEALER.deal_card()

GAMBLER.print_current_hand_and_value()
print
DEALER.print_current_hand_and_value()

# Main logic - Check for WIN on OPEN

if GAMBLER.check_win():
    print 'Gambler gets BlackJack on open!'
    game_over = True
    winner = 'Gambler'
elif GAMBLER.check_bust():
    print 'Gambler busts on open!'
    game_over = True
    winner = 'Dealer'

if DEALER.check_win():
    print 'Dealer gets BlackJack on open!'
    game_over = True
    winner = 'Dealer'
elif DEALER.check_bust():
    print 'Dealer busts on open!'
    game_over = True
    winner = 'Gambler'

# Main logic - If nobody wins on Open

while not game_over:

    while not gambler_turn_over:
        if GAMBLER.check_win():
            gambler_turn_over = True
            game_over = True
            winner = 'GAMBLER'
            print
            print 'Gambler hits 21!!'
        elif GAMBLER.check_bust():
            winner = 'DEALER'
            print
            print 'Gambler hits bust!!!'
            gambler_turn_over = True
            game_over = True
        else:
            GAMBLER.gambler_turn()

    if not game_over:
        while not dealer_turn_over:
            if DEALER.check_win():
                print
                winner = 'DEALER'
                print 'Dealer hits 21!!'
                dealer_turn_over = True
                game_over = True
            elif DEALER.check_bust():
                print
                winner = 'Gambler'
                print 'Dealer hits bust!!'
                dealer_turn_over = True
                game_over = True
            else:
                DEALER.dealer_turn()

    if not game_over:
        GAMBLER.check_use_hard_or_soft()
        DEALER.check_use_hard_or_soft()
        GAMBLER.check_winning_hand(GAMBLER, DEALER)
        game_over = True

print
print
print 'Winner of the hand is %s' % winner



















