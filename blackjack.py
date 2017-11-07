"""
BlackJack Game!
Has a number of Gamblers versus an automated dealer.
Dealer hits on 17!

Authors: DL, ML
"""
from random import shuffle


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return '{} of {}'.format(self.value, self.suit)


class Deck:
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
    def __init__(self, bank, player_number):
        Player.__init__(self)
        self.bank = bank
        self.player_number = player_number
        self.active_this_hand = True
        self.active_this_game = True
        self.bank = bank
        self.current_bet = 0

    def win(self):
        if self.choose_hard_or_soft_value() == 21:
            self.active_this_hand = False
            self.bank += (self.current_bet * 2)

    def lose(self):
        if self.choose_hard_or_soft_value() > 21:
            self.active_this_hand = False
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
                print 'Player {} loses by bust!'.format(self.player_number)
            elif self.choose_hard_or_soft_value() == 21:
                still_going = False
                self.active_this_hand = False
                self.win()
                print 'Player {} wins at 21!'.format(self.player_number)
            else:
                print '\nDealers face up card: {}'.format(dealer_faceup_card)
                # print 'Your current hand contains: {} \nValue" {}'.format(self.print_entire_hand(), self.choose_hard_or_soft_value())
                ask_player_turn = raw_input("\nEnter your next move!\nOptions:\n\t'Hit'\n\t'Stay'\n\t'Bet' \n").lower()
                if ask_player_turn == 'hit':
                    # card = self.add_card_to_hand(self.deck.deal_card_from_deck())
                    card = deck.deal_card_from_deck()
                    print 'You got the {}!\n'.format(card)
                    self.hand.append(card)
                elif ask_player_turn == 'stay':
                    still_going = False
                    self.active_this_hand = False
                elif ask_player_turn == 'bet':
                    self.add_to_bet()
                else:
                    print 'Invalid input. Please try again'


class Dealer(Player):
    def __init__(self):
        Player.__init__(self)
        self.dealer_wins = False
        self.dealer_went_bust = False
        self.dealer_turn_over = False

    def win(self):
        if self.choose_hard_or_soft_value() == 21:
            self.dealer_wins = True

    def lose(self):
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
            # while self.choose_hard_or_soft_value() <= 16:
            self.add_card_to_hand(deck.deal_card_from_deck())
            self.print_dealer_full_hand_and_value()
            if self.choose_hard_or_soft_value() > 21:
                dealer_still_going = False
            elif self.choose_hard_or_soft_value() == 21:
                dealer_still_going = False


class Game:
    def __init__(self):
        self.d = Deck(2)
        self.players = []
        self.deal = Dealer()
        self.num_active_players = 0
        self.buy_in = 5


    def start_game(self):
        self.d.shuffle_deck()
        ask_complete = False
        while not ask_complete:
            ask_num_players = raw_input('\nWelcome to Blackjack! How many players? \nSelect 1, 2, 3 or 4\n')
            if ask_num_players.isdigit():
                if int(ask_num_players) > 0 and int(ask_num_players) <= 4:
                    for p in range(int(ask_num_players)):
                        self.players.append(Gambler(50, p + 1))
                        ask_complete = True
                else:
                    print 'Choose number between 1 and 4'
            else:
                print 'Invalid input. Please enter number between 1-4'

        self.play()

    def play(self):
        for p in self.players:
            if p.bank < 5:
                print 'Player {} does not have enough money to play!'.format(p.player_number)
                p.active_this_game = False
            else:
                # self.num_active_players += 1
                p.clear_hand()
                p.bank -= self.buy_in
                p.current_bet += self.buy_in
                p.add_card_to_hand(self.d.deal_card_from_deck())
                p.add_card_to_hand(self.d.deal_card_from_deck())
                self.deal.clear_hand()
                self.deal.add_card_to_hand(self.d.deal_card_from_deck())

        for p in self.players:
            if p.active_this_game:
                print
                print
                print '<----------------->'
                print '<----------------->'
                print '<----------------->'
                print '<----------------->'
                print
                print "Player {}'s turn!".format(p.player_number)
                print
                print '<----------------->'
                print '<----------------->'
                print '<----------------->'
                print '<----------------->'
                p.take_turn(self.deal.get_faceup_card(), self.d)

        print '<----------------->'
        print '<----------------->'
        print
        print 'Dealers turn!'
        print
        print '<----------------->'
        print '<----------------->'
        self.deal.dealer_take_turn(self.d)
"""
for p in player:

"""
        for p in self.players:
                # if p.choose_hard_or_soft_value > self.deal.choose_hard_or_soft_value():
            print 'Player {} score: {} | Dealer score: {}'.format(p.player_number, p.choose_hard_or_soft_value(), self.deal.choose_hard_or_soft_value())
            if p.choose_hard_or_soft_value() > self.deal.choose_hard_or_soft_value() and p.choose_hard_or_soft_value < 22:
                p.win()
                print 'Player {} wins {}!! Bank: {}'.format(p.current_bet, p.player_number, p.bank)
            elif self.deal.choose_hard_or_soft_value() > p.choose_hard_or_soft_value() and self.deal.choose_hard_or_soft_value() < 22:
                print 'Dealer wins! Player {} loses {}!'.format(p.player_number, p.current_bet)











# This will run every time a hand is played
# Check if players have enough money to play
# If not, take them out of active players?
# If so, reduce bank by buy in
# deal 2 cards to each player
# deal one faceup card to dealer
# Ask each player to play
# make dealer play
# assess immediate wins/losses
# assess win by higher number for all players & dealer
# print out all winners


the_game = Game()
the_game.start_game()

# d = Deck(1)
# d.shuffle_deck()
#
# gambler = Gambler(50, 1)
# gambler.add_card_to_hand(d.deal_card_from_deck())
# gambler.add_card_to_hand(d.deal_card_from_deck())
#
# dealer = Dealer()
# dealer.add_card_to_hand(d.deal_card_from_deck())
# dealer.add_card_to_hand(d.deal_card_from_deck())
#
# gambler.take_turn(dealer.get_faceup_card(), d)




# print 'Gambler stuff'
# g = Gambler(50, 1)
# g.add_card_to_hand(d.deal_card_from_deck())
# g.add_card_to_hand(d.deal_card_from_deck())
# g.add_card_to_hand(d.deal_card_from_deck())
#
# g.print_entire_hand()
# g.print_hand_value()
#
# print
# print 'Dealer stuff'
# deal = Dealer()
# deal.add_card_to_hand(d.deal_card_from_deck())
# deal.add_card_to_hand(d.deal_card_from_deck())
# deal.add_card_to_hand(d.deal_card_from_deck())
# deal.print_dealer_full_hand_and_value()
# print deal.get_faceup_card()
