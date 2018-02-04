"""
BlackJack Game!
Has a number of Gamblers versus an automated dealer.
Number of players in determined at beginning by user input.
Dealer hits on 17!

Authors: DL, ML
"""

from random import shuffle


class Card(object):
    """
    Card class. Makes Card object which has a suit and value.
    """
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.points = self.get_card_points()

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)

    def get_card_points(self):
        """
        Runs when a Card is instantiated
        Assigns each card a points value
        :return: int to be used for self.points attribute
        """
        return (10 if self.value in ('Jack', 'King', 'Queen')
                else 1 if self.value == 'Ace'
                else int(self.value))


class Deck(object):
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
        full_deck = [Card(str(v), s) for v in values for s in suits]
        for i in range(self.number_of_decks):
            self.all_decks += full_deck

    def deal_card_from_deck(self):
        """
        Pops card from Deck and returns it
        """
        return self.all_decks.pop()

    def shuffle_deck(self):
        """
        Uses import shuffle to shuffle Deck
        """
        shuffle(self.all_decks)


class Player(object):
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
        for card in self.hand:
            print card

    def check_natural_win(self):
        """
        Makes a set of all values of cards in hand
        Checks length of set is 2, Ace is in hand and set is subset of facecards
        :return: True if set has length of two & another face card else False
        """
        hand_set = set(card.value for card in self.hand)
        return len(hand_set) == 2 and 'Ace' in hand_set \
            and hand_set < {'Ace', 'Jack', 'King', 'Queen'}

    def get_soft_hand_value(self):
        """
        Calculates hand value with Ace as 1
        :return: int
        """
        return (21.1 if self.check_natural_win()
                else sum(card.points for card in self.hand))

    def get_hand_value(self):
        """
        Calculates hand value with any Ace as 11 as long as it doesn't lead to bust
        :return: int
        """
        if self.check_natural_win():
            return 21.1
        else:
            hand_total = self.get_soft_hand_value()
            if hand_total <= 11 and any(card.value == 'Ace' for card in self.hand):
                hand_total += 10
            return hand_total

    def choose_hard_or_soft_value(self):
        """
        Calls calc hard & soft value methods.
        If hard value makes player go bust, return hard.
        Else return soft.
        :return: int
        """
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hand_value()
        if hard_value >= 22:
            return soft_value
        else:
            return hard_value

    def print_hand_and_value(self):
        """
        Prints entire hand and returns value of hand.
        Returns both hard and soft value if Player has Ace and hard value won't go bust
        :return: Entire hand(list) and string showing value of hand
        """
        for card in self.hand:
            print card
        soft_value = self.get_soft_hand_value()
        hard_value = self.get_hand_value()
        if hard_value == 21.1 or soft_value == 21.1:
            print '\nHand value is Natural 21!'
        elif hard_value == soft_value or hard_value >= 22:
            print '\nHand value is {}'.format(self.get_soft_hand_value())
        else:
            print '\nSoft hand value is {} ' \
                  '\nHard hand value is: {}'.format(self.get_soft_hand_value(),
                                                    self.get_hand_value())


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
        self.bank = bank
        self.current_bet = 0

    def win(self):
        """
        Adds current bet multiplied by 2 to Gamblers Bank
        """
        if self.choose_hard_or_soft_value() == 21.1:
            self.bank += (self.current_bet * 2.5)
        else:
            self.bank += (self.current_bet * 2)

    def lose(self):
        """
        Subtracts Current bet from Gambler bank.
        Gambler will lose buy in when taken so this subtracts anything above buy in.
        :return:
        """
        if self.current_bet > 5:
            self.bank -= (self.current_bet - 5)

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
            if self.choose_hard_or_soft_value() >= 22:
                still_going = False
                self.active_this_hand = False
                self.lose()
                print '<----------------->'
                print
                print 'Player {} loses by bust! Bank now: {}'.format(self.player_number, self.bank)
                print
                print '<----------------->'
            elif self.choose_hard_or_soft_value() == 21.1:
                still_going = False
                self.active_this_hand = False
                self.win()
                print '<----------------->'
                print
                print 'Player {} wins with a natural!!! ' \
                      'Bank now: {}'.format(self.player_number, self.bank)
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
                ask_player_turn = raw_input("\nEnter your next move!"
                                            "\nOptions:\n\t'Hit'\n\t'Stay'\n\t'Bet' \n").lower()
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

    def print_dealer_hand_and_value(self):
        """
        Prints Dealer hand and value, extends print_hand_and_value method in Player to add string.
        :return:
        """
        print '\nDealers entire hand:'
        Player.print_hand_and_value(self)

    def dealer_take_turn(self, deck):
        """
        Dealers turn.
        Continues while dealer is <= 16 and does not Win or Bust.
        :param deck:
        :return:
        """
        dealer_still_going = True
        dealer_new_card = deck.deal_card_from_deck()
        print 'Dealer drew: {}'.format(str(dealer_new_card))
        self.add_card_to_hand(dealer_new_card)
        self.print_dealer_hand_and_value()
        while dealer_still_going and self.choose_hard_or_soft_value() < 17:
            dealer_new_card = deck.deal_card_from_deck()
            print 'Dealer drew: {}'.format(str(dealer_new_card))
            self.add_card_to_hand(dealer_new_card)
            self.print_dealer_hand_and_value()
            if self.choose_hard_or_soft_value() >= 22:
                print 'Dealer busts!'
                dealer_still_going = False
                self.dealer_went_bust = True
            elif self.choose_hard_or_soft_value() == 21.1:
                dealer_still_going = False
                print 'Dealer gets a natural!'
            elif self.choose_hard_or_soft_value() == 21:
                dealer_still_going = False
                print 'Dealer hits 21!'


class Game(object):
    """
    Game Class. Controls game Setup and Play
    """
    def __init__(self):
        self.deck = Deck(10)
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
        for player in self.players:
            if player.active_this_hand:
                count += 1
        return count

    def get_num_active_game(self):
        """
        Returns num of active Gamblers this game. (Not broke)
        :return: int
        """
        count = 0
        for player in self.players:
            if player.active_this_game:
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

        print '<------------------------------------->'
        print 'Player {} Score: {} | Dealer Score: {}' \
              ''.format(gambler.player_number, gambler.choose_hard_or_soft_value(),
                        self.deal.choose_hard_or_soft_value())
        print '<------------------------------------->'
        print

        if dealer_bust:
            gambler.win()
            print 'Player {} Wins! Bank now: {}'.format(gambler.player_number, gambler.bank)
            print
        elif gambler_score > dealer_score:
            gambler.win()
            print 'Player {} Wins! Bank now: {}'.format(gambler.player_number, gambler.bank)
            print
        elif dealer_score > gambler_score:
            gambler.lose()
            print 'Player {} Loses! Bank now: {}'.format(gambler.player_number, gambler.bank)
            print
        elif gambler_score == dealer_score:
            gambler.bank += gambler.current_bet
            print 'Player {} ties with Dealer! Bet Returned. ' \
                  'Bank now: {}'.format(gambler.player_number, gambler.bank)
            print

    def ask_number_of_players(self):
        """
        Runs at start of game.
        Takes user input to determine how many Gamblers in game
        Uses recursion to run until valid answer given
        :return:
        """
        ask_how_many_players = raw_input('\nWelcome to Blackjack! '
                                         'How many players? \nSelect 1, 2, 3 or 4\n')
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
        self.deck.shuffle_deck()
        user_answer = self.ask_number_of_players()
        for player in range(user_answer):
            self.players.append(Gambler(50, player + 1))
            self.num_active_players += user_answer

    def fresh_hand_setup(self, gambler):
        """
        Runs at beginning of each hand.
        Resets values that should be cleared upon new hand
        Clears Hand of Dealer & Gambler, current_bet.
        Also resets boolean win/lose values
        :param gambler: gambler is iterating through self.players list
        :return:
        """
        gambler.clear_hand()
        gambler.active_this_hand = True
        gambler.bank -= self.buy_in
        gambler.current_bet = self.buy_in
        gambler.add_card_to_hand(self.deck.deal_card_from_deck())
        gambler.add_card_to_hand(self.deck.deal_card_from_deck())
        self.deal.clear_hand()
        self.deal.add_card_to_hand(self.deck.deal_card_from_deck())
        self.deal.dealer_went_bust = False

    def play(self):
        """
        Controls the flow of the game
        If Gambler has enough money to buy in, runs their turn.
        If not all Gamblers win/bust, runs Dealers turn.
        For all Gamblers not win/bust, prints out their score Vs Dealer score and determines winner.
        """
        while self.num_active_players > 0:
            for gambler in self.players:
                if gambler.bank < 5:
                    print 'Player {} does not have enough money to play!' \
                          ''.format(gambler.player_number)
                    gambler.active_this_game = False
                    gambler.active_this_hand = False
                    self.num_active_players -= 1
                else:
                    self.fresh_hand_setup(gambler)

            for gambler in self.players:
                if gambler.active_this_game:
                    print_gambler_turn(gambler)
                    gambler.take_turn(self.deal.get_faceup_card(), self.deck)

            if self.get_num_active_hand() > 0:
                print_dealer_turn()
                self.deal.dealer_take_turn(self.deck)
                print_final_results_lines()

            for gambler in self.players:
                if gambler.active_this_hand:
                    self.dealer_or_player_score_win(gambler)

        print 'Thanks for playing!'


def print_gambler_turn(gambler):
    """
    Pretty lines to print Players turn and details
    :param gambler: g is list of Gamblers
    :return: Returns string with Player num & bank
    """
    print
    print '<----------------->'
    print '<----------------->'
    print
    print "Player {}'s turn! Bank: {}".format(gambler.player_number, gambler.bank)
    print
    print '<----------------->'
    print '<----------------->'


def print_dealer_turn():
    """
    Pretty lines to print before Dealers turn
    :return: Some pretty Strings
    """
    print
    print '<----------------->'
    print '<----------------->'
    print
    print 'Dealers turn!'
    print
    print '<----------------->'
    print '<----------------->'


def print_final_results_lines():
    """
    Prints pretty lines/header for final results
    :return: Pretty lines
    """
    print
    print '<----------------->'
    print 'Final Hand Results: '
    print '<----------------->'
    print


THE_GAME = Game()
THE_GAME.setup_game()
THE_GAME.play()
