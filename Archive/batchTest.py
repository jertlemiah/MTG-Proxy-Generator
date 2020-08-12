# Author: Jeremiah Plauche

# The batch test file is a compilation of several tests not included in the full proxy gen test

# The outputs include:
#	A console output of which names in a list had valid API calls or had some error

import requests
import json

class DECK:
	CARD_LIMIT = 75 #Only 75 cards can be requested for each API call

	def __init__(self, deckNameA, deckListA, deckNameB, deckListB):
		self.deckNameA = deckNameA
		self.deckListA = deckListA
		self.deckNameB = deckNameB
		self.deckListB = deckListB



		self.combinedList = self.combineLists()
		self.errors = set()		
		self.cardDicts = self.validate()
		#self.cardDicts = self.batchRequest()

		self.appendix = set()


	'''
	def addApp(self,deckSide,card):
		self.appendix.add(thingy)
	'''
	
	def validate(self):
		cardDicts = []
		i = 1
		for line in self.combinedList:
			if line['cardA'] != '':
				try:
					cardDict1 = cardSearch(line['cardA'])
				except:
					self.errors.add(line['cardA'])
			else:
				pass #what do when there is no card?

			if line['cardB'] != '':
				cardDict2 = cardSearch(line['cardB'])
			else:
				pass #what do when there is no card?

			card = {'board' : line['board'],
				'deckNameA' : line['deckNameA'],
				'cardDictA' : cardSearch(line['cardA']),
				'deckNameB' : line['deckNameB'],
				'cardDictB' : cardSearch(line['cardB'])}
			cardDicts.append(card)
			
			try:
				print(i, ',',
					card['board'], ',',
					card['deckNameA'], ',',
					card['cardDictA']['name'], ',',
					card['deckNameB'], ',',
					card['cardDictB']['name'])
			except:
				print('error')
			i = i+1

		for error in self.errors:
			print("Card name error: ", error)

		return cardDicts

	def expandList(self,decklist):
		i = 0
		decklist = decklist.split('\n')
		decklist.pop(-1)

		mainList = []
		sideList = []

		for card in decklist:
			if "SB:" in card:
				i = card.index(' ')
				card = card[i+1:]
				board = "side"
			else:
				board = "main"		

			if card == '': #If there is a blank line
				continue
			if "//Main" in card or "//Sideboard" in card:
				continue

			i = card.index(' ')
			n = int(card[:i])
			name = card[i+1:]
			while n>0:
				if board == 'main':
					mainList.append(name)
				if board == 'side':
					sideList.append(name)
				n -= 1

		return mainList, sideList

	def combineLists(self):
		combinedList = []

		mainA, sideA = self.expandList(self.deckListA)	
		mainB, sideB = self.expandList(self.deckListB)

		nameA = self.deckNameA
		nameB = self.deckNameB

		n1 = n2 = 0
		for cards in mainA:
			n1 = n1+1
		for cards in mainB:
			n2 = n2+1
		for i in range(max(n1,n2)):
			if i >= n1:
				nameA = ''
				cardA = ''
				cardB = mainB[i]
			elif i >= n2:
				nameB = ''
				cardB = ''
				cardA = mainA[i]
			else:
				cardA = mainA[i]		
				cardB = mainB[i]		
			singleCard = {"board": "main",
					"deckNameA": nameA,
					"cardA": cardA,
					"deckNameB": nameB,
					"cardB": cardB}
			combinedList.append(singleCard)

		nameA = self.deckNameA
		nameB = self.deckNameB

		n1 = n2 = 0
		for cards in sideA:
			n1 = n1+1
		for cards in sideB:
			n2 = n2+1
		for i in range(max(n1,n2)):
			if i >= n1:
				nameA = ''
				cardA = ''
				cardB = sideB[i]
			elif i >= n2:
				nameB = ''
				cardB = ''
				cardA = sideA[i]	
			else:
				cardA = sideA[i]		
				cardB = sideB[i]			
			singleCard = {"board": "side",
					"deckNameA": nameA,
					"cardA": cardA,
					"deckNameB": nameB,
					"cardB": cardB}
			combinedList.append(singleCard)

		return combinedList

	def printList(self):
		i = 1
		for line in self.combinedList:
			print(i, ',',
				line['board'], ',',
				line['deckNameA'], ',',
				line['cardA'], ',',
				line['deckNameB'], ',',
				line['cardB'])
			i = i+1

	def createProxy(board, deck1_name, card1_name, deck2_name, card2_name): #Recieves card names
		width = 750
		height = 525 
		fullCard = Image.new('RGBA', (width, height*2), 'black')
		
		#card1 = cardSearch(card1_name)
		#card2 = cardSearch(card2_name)
		card1 = CARD(side = "A", 
		board = board, 
		deckName = deck1_name,
		cardName = card1_name)

		card2 = CARD(side = "B", 
		board = board, 
		deckName = deck2_name,
		cardName = card2_name)

		card1_image = card1.createImage().rotate(180)
		card2_image = card2.createImage()

		card1_area = (0,0,width,height)
		card2_area = (0,height,width,height*2)

		fullCard.paste(card1_image,card1_area)
		fullCard.paste(card2_image,card2_area)

		if board == "side":
			point1 = (x1,y1) = (width/2-25,height-25)
			point2 = (x2,y2) = (width/2+25,height+25)

			drawCanvas = ImageDraw.Draw(fullCard)

			inc = 3
			round_rectangle2 (canvas = drawCanvas, 
				point1 = (x1-inc,y1-inc), 
				point2 = (x2+inc,y2+inc), 
				radius = 10, 
				fillLeft = 'black', fillRight = 'black')

			round_rectangle2 (canvas = drawCanvas, 
				point1 = point1, point2 = point2, 
				radius = 10, 
				fillLeft = 'white', fillRight = 'white')

			#drawCanvas.text((x1, y1), 
			#	text = 'SB', 
			#	font = fnt_Bel_lg, 
			#	fill = 'Black')

		#fullCard.save("Full Card.png")

		#fullCard.show()
		return fullCard

'''
deck = DECK(deckNameA = deckNameA, 
	deckListA = listA,
	deckNameB = deckNameB,
	deckListB = listB)
'''

sample_deckNames = ('Bant Spirits','BR Hollow One')
sample_deckList = {
'Bant Spirits': "//Main"
	+ "\n2 Anafenza, Kin-Tree Spirit"
#	+ "\n1 Birds of Paradise"
#	+ "\n2 Breeding Pool"
#	+ "\n2 Cavern of Souls"
#	+ "\n4 Collected Company"
#	+ "\n4 Drogskol Captain"
#	+ "\n3 Flooded Strand"
#	+ "\n1 Forest"
#	+ "\n1 Gavony Township"
#	+ "\n1 Hallowed Fountain"
#	+ "\n1 Island"
#	+ "\n1 Kira, Great Glass-Spinner"
#	+ "\n4 Mausoleum Wanderer"
#	+ "\n4 Misty Rainforest"
#	+ "\n4 Noble Hierarch"
#	+ "\n2 Path to Exile"
#	+ "\n1 Plains"
#	+ "\n4 Rattlechains"
#	+ "\n1 Razorverge Thicket"
#	+ "\n2 Seachrome Coast"
#	+ "\n4 Selfless Spirit"
	+ "\n4 Spell Queller"
#	+ "\n3 Supreme Phantom"
#	+ "\n1 Temple Garden"
	+ "\n3 Windswept Heath"
	+ "\nHuntmaster of the Fells"	#Test: transform creature
	+ "\n1 Bruna, the Fading Light"	#Test: meld creature
	+ "\n1 blah"						#Test: invalid card name
	+ "\n1 blah"						#Test: invalid card name
	+ "\n2 Wear // Tear"
	+ "\n2 Faithful Squire" #Test: flip creature
	+ "\n"
	+ "\n//Sideboard"
#	+ "\nSB: 2 Engineered Explosives"
	+ "\nSB: 1 Kira, Great Glass-Spinner"
#	+ "\nSB: 2 Negate"
#	+ "\nSB: 2 Path to Exile"
#	+ "\nSB: 2 Qasali Pridemage"
#	+ "\nSB: 3 Rest in Peace"
	+ "\nSB: 3 Stony Silence",

'BR Hollow One': "//Main"
	+ "\n3 Blackcleave Cliffs"
	+ "\n3 Blood Crypt"
	+ "\n4 Bloodghast"
	+ "\n4 Bloodstained Mire"
	+ "\n4 Burning Inquiry"
	+ "\n2 Collective Brutality"
	+ "\n4 Faithless Looting"
	+ "\n4 Flameblade Adept"
	+ "\n4 Flamewake Phoenix"
	+ "\n4 Goblin Lore"
	+ "\n3 Gurmag Angler"
	+ "\n4 Hollow One"
	+ "\n4 Lightning Bolt"
	+ "\n2 Mountain"
	+ "\n2 Scalding Tarn"
	+ "\n1 Stomping Ground"
	+ "\n4 Street Wraith"
	+ "\n1 Swamp"
	+ "\n1 Tasigur, the Golden Fang"
	+ "\n2 Wooded Foothills"
	+ "\n"
	+ "\n//Sideboard"
	+ "\nSB: 2 Ancient Grudge"
	+ "\nSB: 2 Engineered Explosives"
	+ "\nSB: 3 Fatal Push"
	+ "\nSB: 3 Grim Lavamancer"
	+ "\nSB: 3 Leyline of the Void"
	+ "\nSB: 2 Thoughtseize"
}
'''
names =[
		"Gavony Township",			#utility lands should not have multicolor border. ughhhh
		"Urborg, Tomb of Yawgmoth", #weird single exception, needs to be black
		"Windswept Heath",			#Test: fetchland color border despite colorless color ID
		"Aether Hub",				#Test: gold border for land that taps for any color

		"Plains",					#Test: basic land
		"Hallowed Fountain",		#Test: nonbasic, dual color fetchable land w/ watermarks
		"Cinder Glade",				#Test: nonbasic, dual color fetchable land w/ watermarks
		"Canyon Slough",			#Test: nonbasic, dual color fetchable land w/ watermarks
		"Madblind Mountain",		#Test: nonbasic, single color fetchable land w/ watermark

		"Huntmaster of the Fells",	#Test: transform creature
		"Bruna, the Fading Light",	#Test: meld creature
		"Echo Mage",				#Test: leveler creature
		"Faithful Squire // Kaiso, Memory of Loyalty", #Test: flip creature

		"Bonfire of the Damned",	#Test: miracle card
		"Start // Finish",			#Test: aftermath split card
		"Wear // Tear",				#Test: fuse split card
		"Triumph of Gerard",		#Test: Saga card 		***

		"Tarmogoyf",				#Test: * in power/toughness
		"Walking Ballista",			#Test: x cost, 0/0 creature
		"Nicol Bolas, God-Pharaoh",	#Test: SO MUCH TEXT, also planeswalker
		"Gideon, Ally of Zendikar",	#Test: planeswalker with a +, -, and 0

		"Tasigur, the Golden Fang",	#Test: split mana in card text, split mana next to normal mana
		"Vault Skirge",				#Test: phyrexian mana in cost and card text
		"Boros Reckoner",			#Test: color/color split mana in mana cost
		"Reaper King",				#Test: color/2 split mana cost and card text

		"blah",						#Test: invalid card name
		]

identifiers = []
for name in names:
	identifiers.append({'name': name})

print(identifiers)

data = {
	"identifiers": 
		identifiers
}
url = 'https://api.scryfall.com/cards/collection?'
dicts = requests.post(url, json = data)
dicts = dicts.json()

#print(dicts['object'])

print("Invalid Cards")
for i, card in enumerate(dicts['not_found']):
	print(i, card['name'])

print("Valid Cards")
for i, card in enumerate(dicts['data']):
	print(i, card['name'])

appendix = []
print("Appendix Cards")
for i, card in enumerate(dicts['data']):
	if card['layout'] == 'transform' or card['layout'] == 'flip':
		appendix.append((card['card_faces'][0]['name'],card['card_faces'][1]['name']))
	elif card['layout'] == 'meld':
		appendix.append((card['all_parts'][0]['name'],card['all_parts'][1]['name']))

for card in appendix:
	print(card)
'''
def expandList(deckList):
	i = 0
	deckList = deckList.split('\n')

	mainList = []
	sideList = []

	for card in deckList:
		if card == '': #If there is a blank line
			continue		
		elif "//" in card[0:2]: #Title, i.e. '//Mainboard'
			continue

		if "SB:" in card:
			i = card.index(' ')
			card = card[i+1:]
			board = "side"
		else:
			board = "main"		
		if card[0].isdigit():
			i = card.index(' ')
			qty = int(card[:i])
			name = card[i+1:]
		else:
			qty = 1
			name = card

		while qty>0:
			if board == 'main':
				mainList.append(name)
			if board == 'side':
				sideList.append(name)
			qty -= 1

	return mainList, sideList

def processList(deckList, deckName):
	#name, qty, deck, board
	mainList, sideList = expandList(deckList = deckList)
	for card in mainList:
		print(card)
	for card in sideList:
		print('SB:',card)

	validCards, invalidCards = batchRequest(names = mainList)
	print('_____Valid_____')
	for card in validCards:
		print(card['name'])
	print('_____Invalid_____')
	for card in invalidCards:
		print(card['name'])
	'''
	processedList = {}

	processedList[name] = {
		'qty': qty,
		'name': name,
		'deck': deckName,
		'board': board}
	'''
	#return processedList
	return mainList, sideList

def batchRequest(names): #Request sets of up to 75 cards
	#Takes a list of card names, returns json dictionaries
	max = 75
	tempList = []
	validCards = invalidCards = []

	for n,name in enumerate(names):
		if n >= max:
			tempVal,tempInval = REQUEST(names = tempList)
			validCards += tempVal
			invalidCards += tempInval
			tempList = []
		tempList.append(name)

	tempVal,tempInval = REQUEST(names = tempList)
	validCards = validCards + tempVal
	invalidCards = invalidCards + tempInval
	
	'''
	identifiers = []
	for name in names:
		identifiers.append({'name': name})
	#MAX REQUEST IS 75 CARDS
	data = {
		"identifiers": 
			identifiers
	}
	url = 'https://api.scryfall.com/cards/collection?'
	dictionaries = requests.post(url = url, json = data)

	return dictionaries.json()

	dictionaries = dictionaries.json()
	validCards = dictionaries['data']
	invalidCards = dictionaries['not_found']
	'''
	return validCards, invalidCards

def REQUEST(names):
	identifiers = []
	for name in names:
		identifiers.append({'name': name})

	data = {
		"identifiers": 
			identifiers
	}
	url = 'https://api.scryfall.com/cards/collection?'

	dictionaries = requests.post(url = url, json = data)
	dictionaries = dictionaries.json()

	validCards = dictionaries['data']
	invalidCards = dictionaries['not_found']

	return validCards, invalidCards

def validateList(processedList):
	dicts = batchRequest(names = processedList.keys())
	'''
	{
	'qty': qty,
	'card': dictionary,
	'deck': deckName,
	'board': board}

	'''

	print("_____Keys:_____")
	for key in processedList.keys():
		print(key)
	print("_____VS Names_____")
	for i, card in enumerate(dicts['data']):
		print(i+1, card['name'])		

	print("_____Invalid Cards_____")
	if dicts['not_found'] == []:
		print('None!')
	else:
		for i, card in enumerate(dicts['not_found']):
			print(i+1, card['name'])


	print("_____Valid Cards_____")
	for i, card in enumerate(dicts['data']):
		print(i+1, card['name'])		
		line = processedList[card['name']]


	appendix = []
	print("_____Appendix Cards_____")
	for i, card in enumerate(dicts['data']):
		if card['layout'] == 'transform' or card['layout'] == 'flip':
			appendix.append((card['card_faces'][0]['name'],card['card_faces'][1]['name']))
		elif card['layout'] == 'meld':
			appendix.append((card['all_parts'][0]['name'],card['all_parts'][1]['name']))

	for card in appendix:
		print(card)

	#return 

processedList = processList(
	deckList = sample_deckList['Bant Spirits'],
	deckName = 'Bant Spirits')



#for line in processedList.items():
#	print(line)

#validatedList = validateList(processedList)
#for line in validatedList:
#	print(line)

#dicts = []

#file = open("scryfall-oracle-cards.json")
'''
for i, name in enumerate(names):
	cardName = name.replace(' ', '%20')	#Replace spaces    
	url = ('https://api.scryfall.com/cards/named?exact=!"%s"' %(cardName))
	card = requests.get(url).json()
	dicts.append(card)
	print(i,card['name'])

for i, card in enumerate(dicts):
	print(i,card['name'])
'''
'''
cardName = 'Heart of Kiran'.replace(' ', '%20')	#Replace spaces    
urls.append('https://api.scryfall.com/cards/named?exact=!"%s"' %(cardName))

cardDict = requests.get(urls).json()

for cards in cardDict:
	print(cards['name'])
'''
'''

def processList(deckList, deckName):
	#name, qty, deck, board
	i = 0
	deckList = deckList.split('\n')
	#deckList.pop(-1)

	processedList = {}

	for card in deckList:
		if card == '': #If there is a blank line
			continue		
		elif "//" in card[0:2]: #Title, i.e. '//Mainboard'
			continue	

		if "SB:" in card:
			i = card.index(' ')
			card = card[i+1:]
			board = "side"
		else:
			board = "main"		

		if card[0].isdigit():
			i = card.index(' ')
			qty = int(card[:i])
			name = card[i+1:]
		else:
			qty = 1
			name = card

		processedList[name] = {
			'qty': qty,
			'name': name,
			'deck': deckName,
			'board': board}

'''
#		processedList.append({
#			'qty': qty,
#			'name': name,
#			'deck': deckName,
#			'board': board})
'''

	return processedList
'''