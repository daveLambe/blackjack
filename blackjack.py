"""
BlackJack Game!
Has a number of Gamblers versus an automated dealer.
Number of players in determined at beginning by user input.
Dealer hits on 17!

Authors: DL, ML
"""

# todo - Make Ace + facecard ONLY == 21.1. and lose is >= 22 (Ace and face card alone wins above all else)

from random import shuffle


class Card:
    """
    Card class. Makes Card object which has a suit and value.
    """
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)


class Deck:
    """
    Deck class
    Makes entire deck using card class.
    Makes number of decks input on instantiation.
    """
    def __init__(self, number_of_decks):
        self.all_decks = []
        self.number_of_decks = number_of_decks
        values = range(2, 11) + 'Jack Queen King Ace'.split()
        suits = 'Hearts Diamonds Spades Clubs'.split()
        full_deck = [Card(str(v), s) for v in values for s in suits]  # todo - Do we need to string this?
        for i in range(self.number_of_decks):
            self.all_decks += full_deck

    def deal_card_from_deck(self):
        return self.all_decks.pop()

    def print_deck_and_length(self):  # todo - remove debug code
        print self.all_decks
        print len(self.all_decks)

    def shuffle_deck(self):
        shuffle(self.all_decks)


class Player:
    """
    Player Class.
    This is the Parent Class for both Gambler and Dealer.
    """
    def __init__(self):
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def print_entire_hand(self):
        for c in self.hand:
            print c

    def get_soft_hand_value(self):
        soft_hand_value = 0
        for c in self.hand:
            if c.value.isdigit():
                soft_hand_value += int(c.value)
            elif c.value == 'Ace':
                soft_hand_value += 1
            else:
                soft_hand_value += 10
        return soft_hand_value

    def get_hard_hand_value(self):
        hard_hand_value = 0
        for c in self.hand:
            if c.value.isdigit():
                hard_hand_value += int(c.value)
            elif c.value == 'Ace':
                hard_hand_value += 11
            else:
                hard_hand_value += 10
        return hard_hand_value

    def choose_hard_or_soft_value(self):
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hard_hand_value()
        if hard_value > 21:
            return soft_value
        else:
            return hard_value

    def print_hand_and_value(self):
        for c in self.hand:
            print c
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hard_hand_value()
        if hard_value == soft_value or hard_value > 21:
            print '\nYour hand value is {}'.format(self.get_soft_hand_value())
        else:
            print '\nYour soft hand value is {} ' \
                  '\nYour hard hand value is: {}'.format(self.get_soft_hand_value(), self.get_hard_hand_value())


class Gambler(Player):
    """
    Gambler class. Number of Gamblers is determined by user input.
    """
    def __init__(self, bank, player_number):
        Player.__init__(self)
        self.bank = bank
        self.player_number = player_number
        self.active_this_hand = True
        self.active_this_game = True
        # self.gambler_went_bust = False
        # self.gambler_got_blackjack = False
        self.bank = bank
        self.current_bet = 0

    def win(self):
        self.bank += (self.current_bet * 2)

    def lose(self):
        if self.current_bet > 5:
            self.bank -= (self.current_bet - 5)
        else:
            self.bank -= self.current_bet

    def print_hand_and_value(self):
        print "\nPlayer {}'s full hand:".format(self.player_number)
        Player.print_hand_and_value(self)

    def add_to_bet(self):
        if self.bank < 5:
            print "You don't have any more money to bet!"
        else:
            answered = False
            while not answered:
                ask_bet = int(raw_input("\nYou can raise bet by multiples of 5"
                                        "\nHow much would you like to bet?"
                                        "\nEnter '0' to cancel bet\n"))
                if ask_bet > self.bank:
                    print 'That is more than you have in your bank! Try again!'
                elif ask_bet % 5 == 0 and ask_bet > 0:
                    print 'You added {} to your current bet'.format(ask_bet)
                    self.current_bet += ask_bet
                    self.bank -= ask_bet
                    print 'Your current bet is now: {}'.format(self.current_bet)
                    answered = True
                elif ask_bet == 0:
                    print 'Bet cancelled'
                    print 'Your current bet is still {}'.format(self.current_bet)
                    print
                    answered = True
                else:
                    print 'Raise by multiples of 5!'

    def take_turn(self, dealer_faceup_card, deck):
        still_going = True
        while still_going:
            self.print_hand_and_value()
            if self.choose_hard_or_soft_value() > 21:
                still_going = False
                self.active_this_hand = False
                self.lose()
                print '<----------------->'
                print
                print 'Player {} loses by bust! Bank now: {}'.format(self.player_number, self.bank)
                print
                print '<----------------->'
            elif self.choose_hard_or_soft_value() == 21:
                still_going = False
                self.active_this_hand = False
                self.win()
                print '<----------------->'
                print
                print 'Player {} wins at 21! Bank now: {}'.format(self.player_number, self.bank)
                print
                print '<----------------->'
            else:
                print '\nDealers face up card: {}'.format(dealer_faceup_card)
                ask_player_turn = raw_input("\nEnter your next move!\nOptions:\n\t'Hit'\n\t'Stay'\n\t'Bet' \n").lower()
                if ask_player_turn == 'hit':
                    card = deck.deal_card_from_deck()
                    print
                    print 'You got the {}!\n'.format(card)
                    self.hand.append(card)
                elif ask_player_turn == 'stay':
                    still_going = False
                elif ask_player_turn == 'bet':
                    self.add_to_bet()
                else:
                    print 'Invalid input. Please try again'


class Dealer(Player):
    """
    Dealer Class for automated Dealer.
    """
    def __init__(self):
        Player.__init__(self)
        self.dealer_wins = False
        self.dealer_went_bust = False
        self.dealer_turn_over = False

    def dealer_win(self):
        if self.choose_hard_or_soft_value() == 21:
            self.dealer_wins = True

    def dealer_lose(self):
        if self.choose_hard_or_soft_value() > 21:
            self.dealer_went_bust = True

    def get_faceup_card(self):
        return self.hand[0]

    def print_dealer_full_hand_and_value(self):
        print '\nDealers entire hand:'
        self.print_entire_hand()
        print '\nDealers hand value: {}'.format(self.choose_hard_or_soft_value())

    def dealer_take_turn(self, deck):
        dealer_still_going = True
        while dealer_still_going and self.choose_hard_or_soft_value() <= 16:
            dealer_new_card = deck.deal_card_from_deck()
            print 'Dealer drew: {}'.format(str(dealer_new_card))
            self.add_card_to_hand(dealer_new_card)
            self.print_dealer_full_hand_and_value()
            if self.choose_hard_or_soft_value() > 21:
                print 'Dealer busts!'
                dealer_still_going = False
                self.dealer_went_bust = True
            elif self.choose_hard_or_soft_value() == 21:
                dealer_still_going = False
                print 'Dealer hits 21!'


class Game:
    """
    Game Class. Controls game Setup and Play
    """
    def __init__(self):
        self.d = Deck(2)
        self.players = []
        self.deal = Dealer()
        self.num_active_players = 0
        self.buy_in = 5

    def get_num_active_hand(self):
        count = 0
        for p in self.players:
            if p.active_this_hand:
                count += 1
        return count

    def get_num_active_game(self):
        count = 0
        for p in self.players:
            if p.active_this_game:
                count += 1
        return count

    def dealer_or_player_score_win(self, gambler):
        dealer_score = self.deal.choose_hard_or_soft_value()
        dealer_bust = self.deal.dealer_went_bust
        gambler_score = gambler.choose_hard_or_soft_value()

        if dealer_bust:
            gambler.win()
            print 'Player {} Wins! Bank now: {}'.format(gambler.player_number, gambler.bank)
        elif gambler_score > dealer_score:
            gambler.win()
            print 'Player {} Wins! Bank now: {}'.format(gambler.player_number, gambler.bank)
        elif dealer_score > gambler_score:
            gambler.lose()
            print 'Player {} Loses! Bank now: {}'.format(gambler.player_number, gambler.bank)
        elif gambler_score == dealer_score:
            gambler.bank += gambler.current_bet
            print 'Player {} ties with Dealer! Bet Returned. Bank now: {}'.format(gambler.player_number, gambler.bank)

    def ask_number_of_players(self):
            ask_how_many_players = raw_input('\nWelcome to Blackjack! How many players? \nSelect 1, 2, 3 or 4\n')
            if ask_how_many_players in ['1', '2', '3', '4']:
                return ask_how_many_players
            else:
                print 'Invalid answer. Choose between 1-4 Players'
                return self.ask_number_of_players()

    def setup_game(self):
        self.d.shuffle_deck()
        user_answer = int(self.ask_number_of_players())
        for p in range(user_answer):
            self.players.append(Gambler(50, p + 1))
            self.num_active_players += user_answer
        self.play()

    def play(self):
        while self.num_active_players > 0:
            for p in self.players:
                if p.bank < 5:
                    print 'Player {} does not have enough money to play!'.format(p.player_number)
                    p.active_this_game = False
                    p.active_this_hand = False
                    self.num_active_players -= 1
                else:
                    p.clear_hand()
                    p.bank -= self.buy_in
                    p.current_bet += self.buy_in
                    p.add_card_to_hand(self.d.deal_card_from_deck())
                    p.add_card_to_hand(self.d.deal_card_from_deck())
                    self.deal.clear_hand()
                    self.deal.add_card_to_hand(self.d.deal_card_from_deck())

            for p in self.players:
                if p.active_this_game:
                    print_gambler_turn(p)
                    p.take_turn(self.deal.get_faceup_card(), self.d)

            if self.get_num_active_hand() > 0:
                print_dealer_turn()
                self.deal.dealer_take_turn(self.d)
                print
                print '<----------------->'
                print 'Final Hand Results: '
                print '<----------------->'
                print

            for p in self.players:
                if p.active_this_hand:
                    print '<------------------------------------->'
                    print 'Player {} Score: {} | Dealer Score: {}'.format(p.player_number,
                        p.choose_hard_or_soft_value(), self.deal.choose_hard_or_soft_value())
                    print '<------------------------------------->'
                    print
                    self.dealer_or_player_score_win(p)

        print 'Thanks for playing!'


def print_gambler_turn(g):
    print
    print '<----------------->'
    print '<----------------->'
    print
    print "Player {}'s turn! Bank: {}".format(g.player_number, g.bank)
    print
    print '<----------------->'
    print '<----------------->'


def print_dealer_turn():
    print
    print '<----------------->'
    print '<----------------->'
    print
    print 'Dealers turn!'
    print
    print '<----------------->'
    print '<----------------->'


the_game = Game()
the_game.setup_game()
