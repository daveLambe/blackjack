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

    def deal_card(self):
        self.current_hand.append(DECK.deck_of_cards[0])
        DECK.remove_dealt_card()

    def print_current_hand_and_value(self):
        self.calc_hand_value()
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

    def check_win(self):
        global game_over
        if self.soft_hand_value == 21 or self.hard_hand_value == 21:
            print self.__class__.__name__, 'has won! - from check win'
            game_over = True
            return True
        # elif self.soft_hand_value > 21 or self.hard_hand_value > 21:
        #     print self.__class__.__name__, 'has bust!'
        #     return True
        else:
            return False

    def check_bust(self):
        global game_over
        if self.soft_hand_value > 21 or self.hard_hand_value > 21:
            print self.__class__.__name__, 'is bust! - from check bust'
            game_over = True
            return True
        else:
            return False

    def check_highest_hand(self):
        global winner
        if GAMBLER.hard_hand_value == DEALER.hard_hand_value:
            print 'Tied hand!'
            winner = 'Nobody!'
        elif GAMBLER.hard_hand_value > DEALER.hard_hand_value:
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
        GAMBLER.print_bankroll()
        ask_player = raw_input('Hit or Stay?')
        if ask_player == 'hit':
            self.deal_card()
            self.print_current_hand_and_value()
            return True
        elif ask_player == 'stay':
            print 'Dealers turn! \nHere is the final Gambler hand'
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
        while self.soft_hand_value < 17 and self.hard_hand_value < 17:
            self.deal_card()
            return True
        # elif self.soft_hand_value == 21 or self.hard_hand_value == 21:
        #     self.print_current_hand_and_value()
        #     game_over = True
        #     print 'Dealer wins at 21! - from dealer turn'
        #     return False
        else:
            # self.print_current_hand_and_value()
            # game_over = True
            # print 'dealer reached at least 17'
            dealer_turn_over = True
            return False

# End Classes


# Start Logic

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
        GAMBLER.gambler_turn()

        if GAMBLER.check_win():
            print 'Gambler wins NOT ON OPEN'
            gambler_turn_over = True
            game_over = True
            winner = 'GAMBLER'
        elif GAMBLER.check_bust():
            print 'Gambler busts NOT ON OPEN'
            winner = 'DEALER'
            gambler_turn_over = True
            game_over = True
        else:
            print 'meow'

    if not GAMBLER.check_win() and not GAMBLER.check_bust():
        while not dealer_turn_over:
            DEALER.dealer_turn()
            DEALER.print_current_hand_and_value()
            if DEALER.check_win():
                print 'Dealer wins NOT ON OPEN'
                winner = 'DEALER'
                dealer_turn_over = True
                game_over = True
            elif DEALER.check_bust():
                print 'Dealer busts NOT ON OPEN'
                winner = 'GAMBLER'
                dealer_turn_over = True
                game_over = True
            else:
                GAMBLER.check_highest_hand()
                game_over = True


print 'Winner of the hand is %s' % winner


# Sudo Main Logic
# Create Deck ---
# Shuffle Deck ---
# Create Gambler ---
# Create Dealer ---
# Give Gambler two cards ---
# Give Dealer two cards ---
# Check if either wins on open ---

# If win:
# present win ---
# ask player if they want to play again
#
# If not win:
# Ask Gambler hit or stay ---
# If hit, deal card ---
# Check if they win - If so, tell win and ask if play again
# Check if they bust - If so, tell lose and ask if play again
#
# Repeat until they say stay
# After stay:
# When they say stay:
# If dealer below 17, give dealer card.
# Check if dealer win
# Check if dealer bust
# Repeat until dealer gets to at least 17
#
# If nobody win or bust by here, simply check who has higher card value or if tie.
# Present winner or tie and ask if player again




















