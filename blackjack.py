"""
BlackJack Game!
Has a Gambler versus an automated dealer.
Dealer hits on 17!
"""
from random import shuffle
# BlackJack Game


class Deck(object):
    """
    Class for a Deck of cards
    """


# Methods

    def __init__(self):
        """
        Uses list comprehension to make a deck of cards.
        """
        values = range(2, 10) + ('Jack King Queen Ace').split()
        suits = 'Diamonds Clubs Spades Hearts'.split()
        self.deck_of_cards = ['%s of %s' % (v, s) for v in values for s in suits]

    def print_deck(self):
        """
        Prints deck
        :return:
        """
        print self.deck_of_cards
        print len(self.deck_of_cards)

    def shuffle_deck(self):
        """
        Uses Shuffle from random to shuffle deck
        :return:
        """
        shuffle(self.deck_of_cards)

    def deal_card(self):
        """
        Deals first card in Deck
        (Deck is shuffled once at start so taking first should be okay)
        :return:
        """
        return self.deck_of_cards[0]

    def remove_dealt_card(self):
        """
        Removes the first card in deck. Only used after dealing, therefore removing the dealt card from deck.
        :return:
        """
        del self.deck_of_cards[0]


class Player(object):
    """
    Class for Player (Gambler or Dealer)
    Has attributes and methods used by both
    """

    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        """
        init for Base Player Class - (Gambler & Dealer)
        :param current_hand: Current cards in hand - List
        :param soft_hand_value: Value of hand using Ace as 1 = int
        :param hard_hand_value: Value of hand using Ace as 11 = int
        :param hit: if you want to hit - Bool
        :param stand: If you want to stand - Bool
        """
        self.current_hand = current_hand
        self.soft_hand_value = soft_hand_value
        self.hard_hand_value = hard_hand_value
        self.hit = hit
        self.stand = stand

# Methods

    def deal_card(self):
        """
        Deals card and appends to hand
        Removes dealt card from Deck
        :return:
        """
        self.current_hand.append(DECK.deck_of_cards[0])
        DECK.remove_dealt_card()

    def print_current_hand_and_value(self):
        """
        Calls method to calc hand value, then prints out all cards in current hand and the value of the hand
        If you have an Ace, it will show soft & hard value
        :return:
        """
        self.calc_hand_value()
        print self.__class__.__name__, 'hand contains:', ', '.join(self.current_hand)
        if self.soft_hand_value != self.hard_hand_value:
            print self.__class__.__name__, 'hand has a Soft Value of', self.soft_hand_value, 'and a Hard Value of', self.hard_hand_value
        else:
            print self.__class__.__name__, 'hand has a value of:', self.hard_hand_value

    def calc_hand_value(self):
        """
        Calculates value of current hand
        :return:
        """
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
        """
        Checks if you have won by hitting 21 with either soft or hard hand value
        :return:
        """
        # Sudo hard vs soft
        # if players hard hand value is greater than 21
        #     players hard hand value = players soft hand value
        global GAME_OVER
        if self.soft_hand_value == 21 or self.hard_hand_value == 21:
            print self.__class__.__name__, 'has won!'
            GAME_OVER = True
            return True
        else:
            return False

    def check_bust(self):
        """
        Checks if soft value is over 21, if so.. bust.
        :return:
        """
        global GAME_OVER
        if self.soft_hand_value > 21:
            print self.__class__.__name__, 'is bust!'
            GAME_OVER = True
            return True
        else:
            return False

    def check_use_hard_or_soft(self):
        """
        Determines if you should/can use soft or hard hand value.
        If your hard and soft value are different (And hard value will not make you bust), then you want to use hard value.
        In this case, your hard value becomes your hard and soft value and you can try use it to win.
        :return:
        """
        print
        if self.soft_hand_value != self.hard_hand_value:
            if self.hard_hand_value < 21:
                self.soft_hand_value = self.hard_hand_value

    def check_winning_hand(self, gam, deal):
        """
        Checks tie or who won
        :param gam:
        :param deal:
        :return:
        """
        global WINNER
        print
        print 'Final score.. \nDealer: %s \nGambler: %s' % (deal.soft_hand_value, gam.soft_hand_value)
        if gam.soft_hand_value == deal.soft_hand_value:
            print 'Tied hand!'
            WINNER = 'Nobody!'
        elif gam.soft_hand_value > deal.soft_hand_value:
            print 'Gambler wins by Higher Valued hand!'
            WINNER = 'Gambler'
        else:
            print 'Dealer wins by Higher Valued hand!'
            WINNER = 'Dealer'


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
        """
        Prints current amount in Gamblers bank
        :return:
        """
        print 'Your bank contains', self.bankroll
        print
        print

    def add_bankroll(self, new_bankroll):
        """
        Adds to Gamblers bankroll
        :param new_bankroll:
        :return:
        """
        self.bankroll += new_bankroll

    def change_bet_amount(self, new_bet_amount):
        """
        Default betting amount is 5, this will allow you to raise. (Not used yet)
        :param new_bet_amount:
        :return:
        """
        self.bet_amount = new_bet_amount

    def gambler_turn(self):
        """
        Goes through flow of gamblers turn
        :return:
        """
        global GAMBLER_TURN_OVER
        # GAMBLER.print_bankroll()
        print
        ask_player = raw_input('Hit or Stay?').lower()
        if ask_player == 'hit':
            self.deal_card()
            self.print_current_hand_and_value()
            return True
        elif ask_player == 'stay':
            print 'Here is the final Gambler hand...'
            self.print_current_hand_and_value()
            GAMBLER_TURN_OVER = True
            return False


class Dealer(Player):
    """
    Subclass - Dealer
    """
    def __init__(self, current_hand=[], soft_hand_value=0, hard_hand_value=0, hit=False, stand=False):
        """
        Creates Dealer subclass
        :param current_hand:
        :param soft_hand_value:
        :param hard_hand_value:
        :param hit:
        :param stand:
        """
        Player.__init__(self, current_hand, soft_hand_value, hard_hand_value, hit, stand)


# Methods

    def dealer_turn(self):
        """
        Goes through flow of dealer turn
        :return:
        """
        global GAME_OVER
        global DEALER_TURN_OVER
        print '\nDealers turn..'
        if self.hard_hand_value < 21:
            if self.hard_hand_value < 17:
                print 'Dealer needs to draw a card..'
                self.deal_card()
                DEALER.print_current_hand_and_value()
                return True
            else:
                print 'Dealer does not need to draw a card..'
                DEALER_TURN_OVER = True
                return False
        elif self.soft_hand_value < 17:
            print 'Dealer needs to draw a card'
            self.deal_card()
            DEALER.print_current_hand_and_value()
            return True
        else:
            print 'Dealer does not need to draw a card'
            DEALER_TURN_OVER = True
            return False


# End Classes

# Sudo Main logic - Start Game

print
print
print "Let's play BlackJack!"
print
print
GAME_OVER = False
GAMBLER_TURN_OVER = False
DEALER_TURN_OVER = False
WINNER = 'blank'
# Create Deck and shuffle
DECK = Deck()
DECK.shuffle_deck()
# Create Gambler, Deal 2 cards
GAMBLER = Gambler()
GAMBLER.deal_card()
GAMBLER.deal_card()

# Create Dealer, Deal 2 cards
DEALER = Dealer()
DEALER.deal_card()
DEALER.deal_card()

GAMBLER.print_current_hand_and_value()
print
DEALER.print_current_hand_and_value()
print

# Main logic - Check for WIN on OPEN

if GAMBLER.check_win():
    print 'Gambler gets BlackJack on open!'
    GAME_OVER = True
    WINNER = 'Gambler'
elif DEALER.check_win():
    print 'Dealer gets BlackJack on open!'
    GAME_OVER = True
    WINNER = 'Dealer'


# Main logic - If nobody wins on Open

if not GAME_OVER:
    while not GAMBLER_TURN_OVER:
        if GAMBLER.check_win():
            GAMBLER_TURN_OVER = True
            GAME_OVER = True
            WINNER = 'GAMBLER'
            print
            print 'Gambler hits 21!!'
        elif GAMBLER.check_bust():
            WINNER = 'DEALER'
            print
            print 'Gambler hits bust!!!'
            GAMBLER_TURN_OVER = True
            GAME_OVER = True
        else:
            GAMBLER.gambler_turn()

if not GAME_OVER:
    while not DEALER_TURN_OVER:
        if DEALER.check_win():
            print
            WINNER = 'DEALER'
            print 'Dealer hits 21!!'
            DEALER_TURN_OVER = True
            GAME_OVER = True
        elif DEALER.check_bust():
            print
            WINNER = 'Gambler'
            print 'Dealer hits bust!!'
            DEALER_TURN_OVER = True
            GAME_OVER = True
        else:
            DEALER.dealer_turn()

# Main logic - Nobody wins or busts - Check Highest Hand Value and declare Winner!

if not GAME_OVER:
    GAMBLER.check_use_hard_or_soft()
    DEALER.check_use_hard_or_soft()
    GAMBLER.check_winning_hand(GAMBLER, DEALER)
    GAME_OVER = True

print
print
print 'Winner of the hand is %s' % WINNER
