# Mini-project #6 - Blackjack by Nick Togneri

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "test"
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    global cards, a_hand, deck_list, player_hand
    
    def __init__(self):
        self.a_hand = []
        # self.card = card
        
    def __str__(self):
            # return a string representation of a hand
        cards = ""
        for i in range(len(self.a_hand)):
             cards += str(self.a_hand[i])+ ' '
        return cards

    def add_card(self, card):
            # add a card object to a hand
        self.a_hand.append(card)

    def get_value(self):
        value = 0
        has_ace = False
        for card in self.a_hand:
            value += VALUES[card.get_rank()]     
            if card.get_rank() == 'A':
                has_ace = True
        if has_ace == True: 
            if value + 10 <= 21:
                value += 10
        return value

    def draw(self, canvas, pos):
        i = 0
        
        for card in self.a_hand:
            card.draw(canvas, ((pos[0]-200)+(i*80),pos[1]))
            i += 1


# define deck class 
class Deck:
    global deck_list
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        for suit in SUITS: 
            for rank in RANKS:
                self.deck_list.append(Card(suit, rank))
        
    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.deck_list)

    def deal_card(self):
        return self.deck_list.pop()
    
    def __str__(self):
        cards = ""
        for i in range(len(self.deck_list)):
            cards += (self.deck_list[i]) 
        return cards	
    # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, a_hand, deck_list, player_hand, deck, dealer_hand, dealer_busts, player_score
    if in_play == True:
        player_score -= 1
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
#    
#    print 'Player Hand:', player_hand
#    print 'Dealer Hand:', dealer_hand
    
    outcome = "Click 'Hit' or 'Stand'"
    dealer_busts = False
    in_play = True

def hit():
    global in_play, deck, outcome, dealer_score
    
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = 'You busted! Click "Deal" again?'
            dealer_score += 1
            in_play = False

    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, deck, dealer_busts, dealer_hand, outcome, player_score, dealer_score
    in_play = False
        
    while dealer_hand.get_value() <= 17:
        dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer Busts! Click "Deal" again?'
            player_score += 1
            dealer_busts = True
                
#    print 'Player: ', player_hand.get_value()
#    print 'Dealer: ', dealer_hand.get_value()
#    print
    
    if dealer_busts != True:
        if dealer_hand.get_value() == player_hand.get_value():
            outcome = 'Tie game, Dealer wins. Click "Deal" again?'
            dealer_score += 1
        elif dealer_hand.get_value() > player_hand.get_value():
            if dealer_busts == False:
                outcome = 'Dealer Wins. Click "Deal" again?'
                dealer_score += 1
        else:
            outcome = 'YOU WIN! Click "Deal" again?'
            player_score += 1


# draw handler    
def draw(canvas):
    global player_hand, in_play, card_loc
    # test to make sure that card.draw works, replace with your code below
    
    
    card = dealer_hand
    card.draw(canvas, [300, 350])
    player_hand.draw(canvas,[300,100])
    canvas.draw_text(('You (current hand = '+ str(player_hand.get_value())+'):'), (20, 80), 26, 'Black')
    if in_play == True:
        canvas.draw_text('Dealer (current hand = ???):', (20, 330), 26, 'Black')
    elif in_play == False:
        canvas.draw_text('Dealer (current hand = ' + str(dealer_hand.get_value()) + '):', (20, 330), 26, 'Black')
    canvas.draw_text(outcome, (20, 250), 30, 'Aqua')
    canvas.draw_text('Won: ' + str(player_score), (20, 110), 20, 'Black') 
                     
    canvas.draw_text('Won: ' + str(dealer_score), (20, 360), 20, 'Black')
    canvas.draw_text('--=:  Blackjack!  :=--', (140, 40), 38, 'Orange')
    if in_play == True:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [136,398], CARD_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 520)
frame.set_canvas_background("Green")

#create buttons and canvas callback


frame.add_label(" ",800)
frame.add_label(" ",800)
frame.add_label(" ",800)
frame.add_label(" ",800)

frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric