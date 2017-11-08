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
        """
        Pops card from Deck and returns it
        :return:
        """
        return self.all_decks.pop()

    def shuffle_deck(self):
        """
        Uses import shuffle to shuffle Deck
        :return:
        """
        shuffle(self.all_decks)


class Player:
    """
    Player Class.
    This is the Parent Class for both Gambler and Dealer.
    """
    def __init__(self):
        self.hand = []

    def add_card_to_hand(self, card):
        """
        Adds card to hand(list) of Player
        """
        self.hand.append(card)

    def clear_hand(self):
        """
        Sets Player hand(list) to empty
        """
        self.hand = []

    def print_entire_hand(self):
        """
        Prints entire Player hand (list)
        """
        for c in self.hand:
            print c

    def get_soft_hand_value(self):
        """
        Calculates hand value with Ace as 1 (Soft hand value)
        :return: int
        """
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
        """
        Calculates hand value with Ace as 11 (Hard hand value)
        :return: int
        """
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
        """
        Calls calc hard & soft value methods.
        If hard value makes player go bust, return hard.
        Else return soft.
        :return: int
        """
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hard_hand_value()
        if hard_value > 21:
            return soft_value
        else:
            return hard_value

    def print_hand_and_value(self):
        """
        Prints entire hand and returns value of hand.
        Returns both hard and soft value if Player has Ace and hard value won't go bust
        :return: Entire hand(list) and string showing value of hand
        """
        for c in self.hand:
            print c
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hard_hand_value()
        if hard_value == soft_value or hard_value > 21:
            print '\nHand value is {}'.format(self.get_soft_hand_value())
        else:
            print '\nSoft hand value is {} ' \
                  '\nHard hand value is: {}'.format(self.get_soft_hand_value(), self.get_hard_hand_value())


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
        """
        Adds current bet multiplied by 2 to Gamblers Bank
        """
        self.bank += (self.current_bet * 2)

    def lose(self):
        """
        Subtracts Current bet from Gambler bank.
        Gambler will lose buy in when taken so this subtracts anything above buy in.
        :return:
        """
        if self.current_bet > 5:
            self.bank -= (self.current_bet - 5)
        # else:
        #     self.bank -= self.current_bet - todo maybe not necessary as buy in is subtracted at start of hand

    def print_hand_and_value(self):
        """
        Prints Player hand and value, extends print_hand_and_value method in Player to add string.
        :return: String, Gambler hand & value
        """
        print "\nPlayer {}'s full hand:".format(self.player_number)
        Player.print_hand_and_value(self)

    def add_to_bet(self):
        """
        Takes user input to add to Gambler current_bet
        Only allows multiple of fives
        Will only allow if Gambler has enough money in bank
        :return:
        """
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
        """
        While Gambler not bust or win, asks Gambler to Hit, Stay or Bet.
        :param dealer_faceup_card: Displayers Dealers face up card as this will factor in decision
        :param deck: Takes instantiation of Deck so Gambler may draw from it
        """
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
        """
        Determines if dealer hits 21, therefore winning.
        :return: return bool
        """
        if self.choose_hard_or_soft_value() == 21:
            self.dealer_wins = True

    def dealer_lose(self):
        """
        Determines if dealer busts by going over 21
        :return: bool
        """
        if self.choose_hard_or_soft_value() > 21:
            self.dealer_went_bust = True

    def get_faceup_card(self):
        """
        Returns first card in dealers hard
        This is "face up" card that Gambler can see while taking their turn
        :return: Card object
        """
        return self.hand[0]

    def print_dealer_full_hand_and_value(self):
        """
        Prints Dealer hand and value, extends print_hand_and_value method in Player to add string.
        :return:
        """
        print '\nDealers entire hand:'
        Player.print_hand_and_value(self)
        # self.print_entire_hand()
        # print '\nDealers hand value: {}'.format(self.choose_hard_or_soft_value())

    def dealer_take_turn(self, deck):
        """
        Dealers turn.
        Continues while dealer is <= 16 and does not Win or Bust.
        :param deck:
        :return:
        """
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
        """
        Return number of active Gamblers in this hand (Not bust or win)
        :return: int
        """
        count = 0
        for p in self.players:
            if p.active_this_hand:
                count += 1
        return count

    def get_num_active_game(self):
        """
        Returns num of active Gamblers this game. (Not broke)
        :return: int
        """
        count = 0
        for p in self.players:
            if p.active_this_game:
                count += 1
        return count

    def dealer_or_player_score_win(self, gambler):
        """
        Determines if Gambler or Dealer wins by higher value
        :param gambler: Takes in Gambler which is iterating through self.players list
        :return:
        """
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
        """
        Runs at start of game. Takes user input to determine how many Gamblers in game
        Uses recursion to run until valid answer given
        :return:
        """
        ask_how_many_players = raw_input('\nWelcome to Blackjack! How many players? \nSelect 1, 2, 3 or 4\n')
        if ask_how_many_players in ['1', '2', '3', '4']:
            return int(ask_how_many_players)
        else:
            print 'Invalid answer. Choose between 1-4 Players'
            return self.ask_number_of_players()

    def setup_game(self):
        """
        Runs at start of game to get things in correct state
        Shuffles Deck
        Uses user input from ask_number_of_players to create that many Gamblers
        Calls play() method to start game once Gmablers created
        :return:
        """
        self.d.shuffle_deck()
        user_answer = self.ask_number_of_players()
        for p in range(user_answer):
            self.players.append(Gambler(50, p + 1))
            self.num_active_players += user_answer
        self.play()

    def fresh_hand_setup(self, p):
        """
        Runs at beginning of each hand.
        Resets values that should be cleared upon new hand
        Clears Hand of Dealer & Gambler, current_bet.
        Also resets boolean win/lose values
        :param p: p is iterating through self.players list
        :return:
        """
        p.clear_hand()
        p.active_this_hand = True
        p.bank -= self.buy_in
        p.current_bet += self.buy_in
        p.add_card_to_hand(self.d.deal_card_from_deck())
        p.add_card_to_hand(self.d.deal_card_from_deck())
        self.deal.clear_hand()
        self.deal.add_card_to_hand(self.d.deal_card_from_deck())
        self.deal.dealer_went_bust = False

    def play(self):
        """
        Controls the flow of the game
        If Gambler has enough money to buy in, runs their turn.
        If not all Gamblers win/bust, runs Dealers turn.
        For all Gamblers not win/bust, prints out their score Vs Dealer score and determines winner.
        """
        while self.num_active_players > 0:
            for p in self.players:
                if p.bank < 5:
                    print 'Player {} does not have enough money to play!'.format(p.player_number)
                    p.active_this_game = False
                    p.active_this_hand = False
                    self.num_active_players -= 1
                else:
                    self.fresh_hand_setup(p)

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
    """
    Pretty lines to print Players turn and details
    :param g: g is list of Gamblers
    :return: Returns string with Player num & bank
    """
    print
    print '<----------------->'
    print '<----------------->'
    print
    print "Player {}'s turn! Bank: {}".format(g.player_number, g.bank)
    print
    print '<----------------->'
    print '<----------------->'


def print_dealer_turn():
    """
    Pretty lines to print before Dealers turn
    :return:
    """
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
