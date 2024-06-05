"""
Kunh Poker

n=3 # of cards, highest card wins

Action
    [1, 0, 0, 0] Fold
    [0, 1, 0, 0] Call
    [0, 0, 1, x] Bet x amount


Game State
    [Total Players, Player Position, CurrentPot, Balance, Turn]

Reward
    Profit: y (profits)
    Loss: y (loss)


Training:
    state = get_state(game)
    action - get_move(state):
        - model.predict()
    reward, game_over, score = game.play_step(action)
    new_state = get_state(game)
    remember
    model.train()

Game (Pygame):
    play_step(action)
        -> reward, game_over, score

Model (PyTorch):
    model.predict(state)
        -> action
"""
import random

# ********** GAME LOGIC ************
class Card:

	def __init__(self, rank, suit):

		self.rank = 0
		self.suit = ''
		self.image_path = ('img/'+str(rank) + str(suit) + '.png')
		self.selected = False

		#convert the rank to an integer so it's easier to compute the winner of a hand
		if rank == 'A':
			self.rank = 14
		elif rank == 'K':
			self.rank = 13
		elif rank == 'Q':
			self.rank = 12
		elif rank == 'J':
			self.rank = 11
		elif rank == 'T':
			self.rank = 10
		else:
			self.rank = int(rank)

		self.suit = suit

	def __str__(self):
		out = ""

		#convert rank back to a word so it's easier to read
		if self.rank == 14:
			out += "Ace"
		elif self.rank == 13:
			out += "King"
		elif self.rank == 12:
			out += "Queen"
		elif self.rank == 11:
			out += "Jack"
		else:
			out += str(self.rank)

		out += ' of '

		#convert the suit to a word so it's easier to read
		if self.suit == 'H':
			out += 'Hearts'
		elif self.suit == 'S':
			out += 'Spades'
		elif self.suit == 'C':
			out += 'Clubs'
		else:
			out += 'Diamonds'

		return out

#only exists for the __str__ function
class Hand:

	def __init__(self, hand):
		self.hand = hand

	def __str__(self):
		out = ""
		for card in self.hand:
			out += str(card) + ", "
		return out

	def __getitem__(self, index):
		return self.hand[index]

	def __len__(self):
		return len(self.hand)

class Deck:

	def __init__(self):
		self.deck = []

		for suit in ['H','S','C','D']:
			for rank in range(2,15):
				self.deck.append(Card(rank, suit))

	def __str__(self):
		out = ""
		for card in self.deck:
			out += str(card) + "\n"
		return out

	def __getitem__(self, index):
		return self.deck[index]

	#return a list a cards taken from the deck
	def deal(self, amount):
		cards = []

		#cap out the cards dealt
		if amount > len(self.deck):
			print("There are not enough cards!  I can only deal " + str(len(self.deck)) + " cards.")
			amount = len(self.deck)

		#create and then return a list of cards taken randomly from the deck
		for i in range(amount):
			card = random.choice(self.deck)
			self.deck.remove(card)
			cards.append(card)
		return cards
class Poker:

	def __init__(self, scores = [0, 0]):
		self.deck = Deck()
		self.scores = scores

		self.playerHand = Hand(self.deck.deal(1))
		self.comp1Hand = Hand(self.deck.deal(1))