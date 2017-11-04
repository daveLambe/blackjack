"""
BlackJack Game!
Has a number of Gamblers versus an automated dealer.
Dealer hits on 17!

Authors: DL, ML
"""
from random import shuffle
# BlackJack Game


class Card:
    """
    Class for a card
    """

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)


class Deck:
    """
    A List of Cards, used both for the Players' hands and the game Deck
    """

    def __init__(self, number_of_decks):
        values = range(2, 11) + ('Jack King Queen Ace').split()
        suits = 'Diamonds Clubs Spades Hearts'.split()
        self.cards = [Card(s,str(v)) for v in values for s in suits]

    def shuffle(self):
        """
        Uses Shuffle from random to shuffle deck
        """
        shuffle(self.cards)

    def deal_card(self):
        """
        Deals first card in Deck and removes it from the Deck
        """
        return self.cards.pop()


class Player:
    """
    Can be the dealer or a real player
    """

    def __init__(self):
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def get_soft_hand_value(self):
        """
        Calculates soft value of current hand
        :return:
        """
        soft_hand_value = 0
        for i in range(len(self.hand)):
            if self.hand[i].value.isdigit():
                soft_hand_value += int(self.hand[i].value)
            elif self.hand[i].value == 'Ace':
                soft_hand_value += 1
            else:
                soft_hand_value += 10
        return soft_hand_value

    def get_hard_hand_value(self):
        """
        Calculates hard value of current hand
        :return:
        """
        hard_hand_value = 0
        for i in range(len(self.hand)):
            if self.hand[i].value.isdigit():
                hard_hand_value += int(self.hand[i].value)
            elif self.hand[i].value == 'Ace':
                hard_hand_value += 11
            else:
                hard_hand_value += 10
        return hard_hand_value

    def print_hand_and_value(self):
        for c in self.hand:
            print c
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hard_hand_value()
        if soft_value == hard_value or hard_value > 21:
            print "Hand Value is {}".format(soft_value)
        else:
            print "Soft Hand Value is {}".format(soft_value)
            print "Hard Hand Value is {}".format(hard_value)
        print

    def get_value_to_use(self):
        h = self.get_hard_hand_value()
        s = self.get_soft_hand_value()
        if h > 21:
            return s
        else:
            return h

class Dealer(Player):
    """
    The enemy...
    """
    active = True

    def ___init__(self):
        Player.__init__()
        self.active = True

    def print_hand_and_value(self):
        print "Dealer's full hand: "
        Player.print_hand_and_value(self)

    def get_faceup_card(self):
        return self.hand[0]

class Gambler(Player):
    def __init__(self, cash, player_number):
        Player.__init__(self)
        self.balance = cash
        self.current_bet = 0
        self.active = True
        self.player_number = player_number

    def print_hand_and_value(self):
        print "Player {}'s full hand: ".format(self.player_number)
        Player.print_hand_and_value(self)

    def change_balance_by(self, delta):
        self.balance += delta

    def ask_increase_bet(self):
        answered = False
        while answered is False:
            ask_bet = int(raw_input("\nThe standard bet is $5. Enter multiple of 5 to add to bet"
                                 " \nType '0' to not add to bet \n"))
            print
            if ask_bet > self.balance:
                print 'You do not have enough money. Please select a smaller amount'
            elif ask_bet % 5 != 0:
                print 'Please enter a multiple of 5'
            elif ask_bet == 0:
                print 'Bet cancelled'
                answered = True
            else:
                self.current_bet += ask_bet
                self.balance -= ask_bet
                print ask_bet, 'added to current bet \nCurrent bet:', self.current_bet
                answered = True

    def take_turn(self, current_dealer_card, deck):
        self.print_hand_and_value()
        print "\nDealer's Face-Up Card:"
        print str(current_dealer_card)
        still_going = True
        while still_going is True:
            ask_player = raw_input("\nOptions:\n\tType 'hit' for a card.\n\tType 'stay' to stick.\n\tType 'bet' to change your bet\n").lower()
            print
            if ask_player == 'hit':
                card = deck.deal_card()
                print "You got the " + str(card)
                self.add_card_to_hand(card)
                self.print_hand_and_value()
                if self.get_value_to_use() > 21:
                    still_going = False
                    self.lose()
                if self.get_value_to_use() == 21:
                    still_going = False
                    self.win()
            elif ask_player == 'stay':
                still_going = False
            elif ask_player == 'bet':
                self.ask_increase_bet()
            else:
                print "Input not recognised."

    def win(self):
        print "Player {} Wins! :D".format(self.player_number)
        self.active = False
        self.change_balance_by(self.current_bet)
        self.current_bet = 0

    def lose(self):
        print "Player {} Loses! D:".format(self.player_number)
        self.active = False
        self.change_balance_by(self.current_bet * -1)
        self.current_bet = 0

class Game():
    """
    The Game
    """

    def __init__(self):
        self.dealer = Dealer()
        self.players = []
        self.num_active_players = 0
        self.deck = Deck(1)

    def setup(self):
        self.deck.shuffle()
        answered = False
        while answered is False:
            ask_player = raw_input("\nWelcome! 1,2,3 or 4 Players?\n")
            print
            if ask_player.isdigit() and int(ask_player) >= 1 and int(ask_player) <= 4:
                ask_player = int(ask_player)
                answered = True
                self.num_active_players = ask_player
                for i in range(ask_player):
                    self.players.append(Gambler(50, i + 1))

    def clear_all_player_hands(self):
        for i in range(len(self.players)):
            self.players[i].clear_hand()

    def get_num_active_players(self):
        count = 0
        for p in self.players:
            if p.active:
                count += 1
        return count

    def play(self):
        the_game.setup()
        for i in [1, 2]:
            for p in self.players:
                p.add_card_to_hand(self.deck.deal_card())
            self.dealer.add_card_to_hand(self.deck.deal_card())


        for i in range(len(self.players)):
            print "\n\n\nPlayer {}'s turn!\n".format(i+1)
            self.players[i].take_turn(self.dealer.get_faceup_card(), self.deck)
        
        if self.get_num_active_players() > 0:
            self.dealer.print_hand_and_value()

        for i in range(len(self.players)):
            if self.players[i].active is True:
                player_score = self.players[i].get_value_to_use()
                dealer_score = self.dealer.get_value_to_use()
                print "Player: {} | Dealer: {}".format(player_score, dealer_score)
                if player_score > dealer_score:
                    self.players[i].win()
                else:
                    self.players[i].lose()

        print "Game Over!"
        self.game_over()

    def game_over(self):
        print "Thanks for Playing!"

#Let's do this!
the_game = Game()
the_game.play()
