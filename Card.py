# -----------------------------------------------------------
# class for storing information regarding a card, which is 
# made of two card-halves
#
# 2021 Jeremiah Plauche, Texas, US
# email jeremiah.plauche@gmail.com
# -----------------------------------------------------------

from Face import Face

class CardHalf:
	def __init__(self, deckName, cardDict):
		self.deckName = deckName

		self.faces = []
		self.faces.append(Face(cardDict, 0))
		if 'card_faces' in cardDict.keys():
			self.faces.append(Face(cardDict, 1))

class Card:
	def __init__(self, board, deck1Name, deck1CardDict, deck2Name, deck2CardDict):
		self.board = board
		self.cardHalfA = CardHalf(deck1Name, deck1CardDict)
		self.cardHalfB = CardHalf(deck2Name, deck2CardDict)
		self.cardHalfC = CardHalf(deck2Name, deck2CardDict)
		

	def printCard(self, simple):
		print("\nFull Card Information")
		print("	Board: " + self.board)
		print("	Side A: " + self.cardHalfA.deckName)
		for face in self.cardHalfA.faces:
			print("		card: " + face.name)
			if not simple: print("			" + str(face.__dict__))
		print("	Side B: " + self.cardHalfB.deckName)
		for face in self.cardHalfB.faces:
			print("		card: " + face.name)
			if not simple: print("			" + str(face.__dict__))