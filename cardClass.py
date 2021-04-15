# Author: Jeremiah Plauche

# Contains the FACE, CARD, & DECK classes, as well as some other useful functions & information
# The file containing the logic for generating the images used for the cards is "createCard.py"

import requests
import json
from PIL import Image, ImageDraw, ImageFont

#_____Colors_____
	#White
color_w = '#CACCC8' #rgb(202,204,200)
color_wMana = '#FCFCC1' #rgb(252,252,193)

	#Blue
color_u = '#127CAC' #rgb(18,124,172)
color_uMana = '#67C1F5' #rgb(103,193,245)

	#Black
color_b = '#363732' #rgb(54,55,50)
#color_bMana = '#848484' #rgb(132,132,132)
color_bMana = '#CCC2C0' #Colorless background

	#Red
color_r = '#D85950' #rgb(216,89,80)
color_rMana = '#F85555' #rgb(248,85,85)
#cr_pale =  '#D8857F' #rgb(216,133,12)

	#Green
color_g = '#1F7751' #rgb(31, 119,81)
#cg_mana = '#26B569' #rgb(38,181,105)
color_gMana = '#90C3A1' #rgb(144,195,161)

	#Colorless
color_cMana = '#CCC2C0' #rgb(204,194,192)

#"Gold" Card
#color_gold = '#D5C089' #rgb(213,192,137)
color_gold = '#B79B52'
#color_gold = '#B99B5F' #rgb(213,175,80)

#_____fonts______________________________________
fnt_Bel_lg = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",35)
fnt_Bel_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",27)
fnt_italic = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MPLANTINIT.TTF",26)

fnt_mana = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",44)
fnt_mana_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",32)
fnt_mana_med = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",70)
#fnt_mana_big = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",100)
#fnt_mana_big2 = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",130)
#fnt_mana_big3 = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",115)
fnt_mana_huge = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",250)

manaCipher = {
	#______MANA CIPHER______________________________#
	# W: white, w: upper white, x: lower white 		#
	# U: blue,	u: upper blue, 	v: lower blue 		#
	# B: black,	b: upper black,	c: lower black 		#
	# R: red,	r: upper red,	s: lower red 		#
	# G: green,	g: upper green, h: lower green 		#
													#
	# E: energy, 	P: phyrexian, 	C: colorless 	#
	# T: tap,		Q: untap, 		S: snow 		#
	# O: mana,		o: lg mana, 	/: split mana 	#
	# .: star,		a: artist, 		X,Y,Z: X,Y,Z 	#
													#
	# 0-9: 0-9										#
	# -: 10, !: 11, @: 12, #: 13, $: 14, %: 15 		#
	# ^: 16, &: 17, *: 18, (: 19, ): 20				#
	#_______________________________________________#

	#Mono mana, color1 "O"; EX: OW. Color2 used in watermark
	"W":  (0, "W", color_wMana, color_wMana),
	"U":  (0, "U", color_uMana, color_u),
	"B":  (0, "B", color_bMana, color_b),
	"R":  (0, "R", color_rMana, color_r),
	"G":  (0, "G", color_gMana, color_g),
	"C":  (0, "C", color_cMana, color_cMana),

	#Other Costs, color1 "O"; EX: OT
	"T":  (0, "T", color_cMana),	#Tap
	"Q":  (0, "Q", color_cMana),	#Untap
	"X":  (0, "X", color_cMana),
	"Y":  (0, "Y", color_cMana),
	"Z":  (0, "Z", color_cMana),
	"S":  (0, "S", color_wMana),	#How to snow?

	#Numbers, color1 "O"; EX: O0
	"0":  (0, "0", color_cMana),
	"1":  (0, "1", color_cMana),
	"2":  (0, "2", color_cMana),
	"3":  (0, "3", color_cMana),
	"4":  (0, "4", color_cMana),
	"5":  (0, "5", color_cMana),
	"6":  (0, "6", color_cMana),
	"7":  (0, "7", color_cMana),
	"8":  (0, "8", color_cMana),
	"9":  (0, "9", color_cMana),
	"10": (0, "-", color_cMana),
	"11": (0, "!", color_cMana),
	"12": (0, "@", color_cMana),
	"13": (0, "#", color_cMana),
	"14": (0, "$", color_cMana),
	"15": (0, "%", color_cMana),
	"16": (0, "^", color_cMana),
	"17": (0, "&", color_cMana),
	"18": (0, "*", color_cMana),
	"19": (0, "(", color_cMana),
	"20": (0, ")", color_cMana),

	#Phyrexian mana, color1 "o"; EX: oP
	"W/P": (1, "P", color_wMana),
	"U/P": (1, "P", color_uMana),
	"B/P": (1, "P", color_bMana),
	"R/P": (1, "P", color_rMana),
	"G/P": (1, "P", color_gMana),

	#Split mana, color1 "o", color2 "/"; EX: o/wv
	"W/U": (2, "wv", color_wMana, color_uMana),
	"W/B": (2, "wc", color_wMana, color_bMana),
	"U/B": (2, "us", color_uMana, color_bMana),
	"U/R": (2, "us", color_uMana, color_rMana),
	"B/R": (2, "bs", color_bMana, color_rMana),
	"B/G": (2, "bh", color_bMana, color_gMana),
	"R/G": (2, "rh", color_rMana, color_gMana),
	"R/W": (2, "rx", color_rMana, color_wMana),
	"G/W": (2, "gx", color_gMana, color_wMana),
	"G/U": (2, "gv", color_gMana, color_uMana),

	"2/W": (2, "`x", color_cMana, color_wMana),
	"2/U": (2, "`v", color_cMana, color_uMana),
	"2/B": (2, "`c", color_cMana, color_bMana),
	"2/R": (2, "`s", color_cMana, color_rMana),
	"2/G": (2, "`h", color_cMana, color_gMana),	

	#Other
	"*": ".",				#Grows the Tarmogoyf
	"E": (3,"E")				#Energy)
}

def cardSearch (card_name):
    cardName = card_name.replace(' ', '%20')	#Replace spaces    
    #base_url = 'https://api.scryfall.com/cards/named?exact=!'	#Base URL
    #final_url = base_url + card_name 			#Final URL
    url = 'https://api.scryfall.com/cards/named?exact=!"%s"' %(card_name) 
    cardDict = requests.get(url=url).json()
    return cardDict

def round_rectangle2 (canvas, point1, point2, radius, fillLeft, fillRight):
    """Draw a rounded, two color rectangle"""
    x1, y1 = point1
    x2, y2 = point2
    xc = x1+(x2-x1)/2

    canvas.ellipse((x1, y1, x1+radius * 2, y1+radius * 2), fill=fillLeft)
    canvas.ellipse((x1, y2-radius * 2, x1+radius * 2, y2), fill =fillLeft)
    canvas.rectangle(((x1,y1+radius),(xc,y2-radius)), fill = fillLeft)
    canvas.rectangle(((x1+radius,y1),(xc,y2)), fill = fillLeft)    

    canvas.ellipse((x2-radius*2, y1, x2, y1+radius * 2), fill=fillRight)
    canvas.ellipse((x2-radius*2, y2-radius * 2, x2, y2), fill=fillRight)
    canvas.rectangle(((xc,y1+radius),(x2,y2-radius)), fill = fillRight)
    canvas.rectangle(((xc,y1),(x2-radius,y2)), fill = fillRight)

class FACE:
	WIDTH = 750
	HEIGHT = 525 
	OFFSET = 20

	Y_NAME = 50 			#offset_name_y = 50
	Y_TEXT = 110 			#offset_text_y = 110
	Y_TYPE = HEIGHT - 95  	#offset_type_y = height - 95  #440

	def __init__(self, faceSide, canvas, drawCanvas, parentDict, cardDict):
		self.faceSide = faceSide #left, right, normal
		self.canvas = canvas
		self.drawCanvas = drawCanvas
		self.layout = parentDict['layout']

		#self.X_LEFT = 65				#limit_left = 65
		#self.X_RIGHT = self.WIDTH - 110	#limit_right = width - 110
		self.LEFT = 0
		self.RIGHT = self.WIDTH
		
		if self.faceSide == 'normal':
			self.LEFT = 0
			self.RIGHT = self.WIDTH
			self.X_LEFT = self.LEFT + 65
			self.X_RIGHT = self.RIGHT - 110

		elif self.faceSide == 'left':
			self.LEFT = 0
			self.RIGHT = self.WIDTH/2
			self.X_LEFT = self.LEFT + 65
			self.X_RIGHT = self.RIGHT - 75

		elif self.faceSide == 'right':
			self.LEFT = self.WIDTH/2
			self.RIGHT = self.WIDTH
			self.X_LEFT = self.LEFT + 20
			self.X_RIGHT = self.RIGHT - 110

		#		if self.layout == 'leveler':
		#			self.X_RIGHT -= 100
		
		self.xoff = 0
		self.yoff = 0
		self.bullets = False												
		self.italics = False												
		self.font = fnt_Bel_sm

		self.populateInfo(cardDict = cardDict)

	def populateInfo(self,cardDict):
		self.name = cardDict['name']
		self.manaCost = cardDict['mana_cost']

		#split card faces do not have a color key
		if self.layout in ('normal','leveler','meld'):
			self.color = cardDict['colors']
			self.colorID = cardDict['color_identity']
			if self.name == 'Urborg, Tomb of Yawgmoth':
				self.colorID = ['B']

		elif self.layout in ('split','flip','transform'):
			mana = ""	
			'''									
			cost = set()																						
			for char in self.manaCost:							
				if char == '}':
					if (mana in ('W','U','B','R','G')):								
						cost.add(mana)						
					mana = ""								
				elif char != '{':							
					mana += char 
			'''
			cost = []																						
			for char in self.manaCost:							
				if char == '}':
					if (mana in ('W','U','B','R','G')):	
						if mana not in cost:							
							cost.append(mana)						
					mana = ""								
				elif char != '{':							
					mana += char 

			self.color = cost
			self.colorID = cost

		self.typeline = cardDict['type_line']
		self.text = cardDict['oracle_text']
		

		if 'Creature' in self.typeline:
			self.powerToughness = (cardDict['power']+"/"+cardDict['toughness'])
		if 'Planeswalker' in self.typeline:
			self.loyalty = cardDict['loyalty']

		i = 0
		colorType = "colorless"
		if 'Land' in self.typeline:
			color = self.colorID 			#I need to fix this. This is not necessarily true
		else:
			color = self.color
		for icon in color:
			if icon in {'W','U','B','R','G'}:
				i += 1
			if i == 1:
				colorType = "monocolor"
			if i == 2:
				colorType = "bicolor"
			if i > 2 or (i == 2 and self.layout == 'split'):
				colorType = "multicolor"

		#Gold land cards
		if 'Land' in self.typeline and ('mana of any color') in self.text:
			colorType = "multicolor"

		#Fetch Lands
		if 'Land' in self.typeline and ('Pay 1 life, Sacrifice') in self.text:
			colorType = "bicolor"
			self.colorID = []
			if "Plains" in self.text:
				self.colorID.append('W')
			if "Island" in self.text:
				self.colorID.append('U')
			if "Swamp" in self.text:
				self.colorID.append('B')
			if "Mountain" in self.text:
				self.colorID.append('R')
			if "Forest" in self.text:
				self.colorID.append('G')

		self.colorType = colorType

		self.text = self.processText(self.text)

	def show(self):
		self.canvas.show()

	def createImage(self):
		self.coloredBorder()
		self.drawTextBox()
		self.drawNameline()
		self.drawTypeline()
		self.drawText()

	def coloredBorder(self):

		(x1,y1) = (self.OFFSET, self.OFFSET)
		(x2,y2) = (self.WIDTH-self.OFFSET, self.HEIGHT-50)

		fill_left = color_cMana
		fill_right = color_cMana
		radius = 40

		if (self.colorType == "multicolor"):
			fill_left = fill_right = color_gold
		else:
			if 'Land' in self.typeline:
				color = self.colorID
			else:
				color = self.color 
			i = 0
			for symbols in color:
				i += 1 

			if i>0:
				fill_left = manaCipher[color[0]][3]
			if i>1:
				fill_right = manaCipher[color[1]][3]

		if(self.colorType == 'monocolor' or 
			self.colorType == 'multicolor' or 
			#self.colorType == 'colorless' or
			#'Basic Land' in self.typeline or
			self.layout == 'split'):
			fill_right = fill_left

		if self.faceSide == 'normal':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')	
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= fill_left, 
				fillRight= fill_right)

		elif self.faceSide == 'left':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')

			x2 = self.WIDTH/2 - 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= fill_left, 
				fillRight= fill_right)
		elif self.faceSide == 'right':
			x1 = self.WIDTH/2 + 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= fill_left, 
				fillRight= fill_right)
			
	def drawTextBox(self):
		(x1,y1) = (self.OFFSET*2+10, 100-30)
		(x2,y2) = (self.WIDTH-self.OFFSET*2-10, self.HEIGHT-100+20)

		if self.faceSide == 'normal':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = 20+inc/2, 
				fillLeft= 'black', fillRight= 'black')	
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = 20+inc/2, 
				fillLeft= 'white', fillRight= 'white')
		elif self.faceSide == 'left':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = 20+inc/2, 
				fillLeft= 'black', fillRight= 'black')

			x2 = self.WIDTH/2 - 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = 20+inc/2, 
				fillLeft= 'white', fillRight= 'white')
		elif self.faceSide == 'right':
			x1 = self.WIDTH/2 + 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = 20+inc/2, 
				fillLeft= 'white', fillRight= 'white')
		if self.layout == 'leveler':
			(x1,y1) = (self.OFFSET*2+10,210)
			(x2,y2) = (self.WIDTH-self.OFFSET*2-10,210)
			self.drawCanvas.line(((x1,y1),(x2,y2)),
				width = 2,
				fill = 'black')
			(x1,y1) = (self.OFFSET*2+10,320)
			(x2,y2) = (self.WIDTH-self.OFFSET*2-10,320)
			self.drawCanvas.line(((x1,y1),(x2,y2)),
				width = 2,
				fill = 'black')		
	def drawText(self):
		if 'Basic Land' in self.typeline:
			self.drawWatermark()
		#		elif self.layout == 'leveler':
		#			self.drawLevel()
		else:
			skip = 0
			if self.layout == 'leveler':
				levelPT = 2
				level = 2
				self.yoff = 15

			trash, self.h = self.drawCanvas.textsize(
				text = "Sample for height reasons", 
				font = fnt_Bel_sm) #comes out to 37	
			self.h -= 4

			for index, word in enumerate(self.text):
				if skip > 0:
					skip -= 1
					continue

				#Leveler Abilities
				if self.layout == 'leveler':
					if '/' in word and not '+' in word and not '-' in word:
						self.drawLevelPT(levelPT,word)
						levelPT += 1
						skip = 1
						continue
					if "LEVEL" in word:
						self.drawLevelBox(level,self.text[index+1])
						if level == 2:
							self.X_LEFT += 100
							self.yoff = 265-45 - self.Y_TEXT
						if level == 3:
							self.yoff = 375-45 - self.Y_TEXT 
						level += 1
						skip = 2
						continue

				#symbol = False		#I don't think this is being used at all?									
				if (word == '\n'):										
					self.yoff += self.h + 7										
					self.xoff = 0											
					self.bullets = False										
					if (word[0]=='•'):									
						self.bullets = True 									
					continue											
				elif "(" in word: 										
					self.italics = True 										
					self.font = fnt_italic	 							
				#__Planeswalker Loyalty___
				if ":" in word and "Planeswalker" in self.typeline:
					self.drawLoyaltyAbility(word)
					continue
					#word = ""

				#__If mana symbol__	
				if "{" in word:	
					word = self.drawManaText(word = word)					
		 																
				#__Printing if not mana/ printing the ending__
				self.drawNormalText(word + ' ') 											
																		
				#__Check for end of italics__							
				if (')' in word):										
					self.italics = False										
					self.font = fnt_Bel_sm								

			landTypes = ('Plains', 'Island','Swamp','Mountain','Forest')
			if any(thing in self.typeline for thing in landTypes):
				self.drawWatermark()
	def drawManaText(self, word):
		begin = ""
		end = ""

		#__Saving the non-mana bits__ 													
		x = word.index("{")									
		begin = word[:x]									
		word = word[x:]																		
		reverse = ""										
		for char in word: 									
			reverse = char + reverse 						
		x = reverse.index("}")								
		if(x!=0):											
			end = word[-(x):]								
			word = word[:-x]																
															
		#__Parsing the mana bits__ 							
		mana = ""											
		cost = []												
		for char in word:									
			if char == '}':									
				cost.append(mana)							
				mana = ""									
			elif char != '{':								
				mana += char 																		
															
		#__Printing the beginning__							
		word = begin
		self.drawNormalText(word) 								
																		
		#__Printing the mana__								
		for mana in cost:									
			mana = manaCipher[mana]							
															
			#If simple mana									
			if mana[0] == 0: 
				self.drawManaSimple(mana) 
																			
			#If Phyrexian mana								
			if mana[0] == 1:
				self.drawManaPhyrexian(mana)														
															
			#If split mana 									
			if mana[0] == 2: 								
				self.drawManaSplit( mana)							
															
			#If other, i.e. energy							
			if mana[0] == 3:
				self.drawManaOther(mana)
		return end		 															 						
	
	def drawNameline(self):
		(x1,y1) = (self.OFFSET*2, self.OFFSET*2+5)
		(x2,y2) = (self.WIDTH-self.OFFSET*2, 100-5)
		#(x1,y1) = (self.LEFT+self.OFFSET*2, self.OFFSET*2+5)
		#(x2,y2) = (self.RIGHT-self.OFFSET*2, 100-5)

		if self.faceSide == 'normal':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = 20+inc/2, 
				fillLeft= 'black', fillRight= 'black')	
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = 20+inc/2, 
				fillLeft= 'white', fillRight= 'white')
		elif self.faceSide == 'left':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = 20+inc/2, 
				fillLeft= 'black', fillRight= 'black')

			x2 = self.WIDTH/2 - 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = 20+inc/2, 
				fillLeft= 'white', fillRight= 'white')
		elif self.faceSide == 'right':
			x1 = self.WIDTH/2 + 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = 20+inc/2, 
				fillLeft= 'white', fillRight= 'white')

		(x1,y1) = (self.LEFT+self.OFFSET*2, self.OFFSET*2+5)
		(x2,y2) = (self.RIGHT-self.OFFSET*2, 100-5)

		trash, h = self.drawCanvas.textsize("Words", 
			font = fnt_Bel_lg)
		yoff = y1 + (y2-y1)/2
		x = self.X_LEFT-10
		y = yoff-h/2-2
		self.drawCanvas.text((x,y), 
			self.name, fill='black', 
			font = fnt_Bel_lg)

		self.drawManacost()

		if "Miracle" in self.text:
			p2 = (x2,y2) = (self.WIDTH/2,self.OFFSET-6)
			p1 = (x1,y1) = (x2-self.OFFSET*2-12,self.OFFSET*2)
			p3 = (x3,y3) = (x2+self.OFFSET*2+12,self.OFFSET*2)
			self.drawCanvas.polygon((p1,p2,p3),
				fill = 'black')

			p2 = (x2,y2) = (self.WIDTH/2,self.OFFSET)
			p1 =(x1,y1) = (x2-self.OFFSET*2,self.OFFSET*2+5)
			p3 =(x3,y3) = (x2+self.OFFSET*2,self.OFFSET*2+5)
			self.drawCanvas.polygon((p1,p2,p3),
				fill = 'white')

	def drawManacost(self):
		#(x1,y1) = (self.OFFSET*2, self.OFFSET*2+5)
		#(x2,y2) = (self.WIDTH-self.OFFSET*2, 100-5)
		(x1,y1) = (self.LEFT+self.OFFSET*2, self.OFFSET*2+5)
		(x2,y2) = (self.RIGHT-self.OFFSET*2, 100-5)

		yoff = y1 + (y2-y1)/2					
		i = 0												
		xoff = -50										
		mana = ""										
		cost = []											
														
		for char in self.manaCost:							
			if char == '}':								
				cost.append(mana)						
				mana = ""								
			elif char != '{':							
				mana += char 												
														
		i = -1											
														
		for blah in cost:								
			mana = manaCipher[cost[i]]					
														
			if mana[0] == 0: #if simple mana 			
				w_letter, h = self.drawCanvas.textsize('O', 					
					font = fnt_mana)					#
																					
				xoff += w_letter + 2					
				x = self.X_RIGHT - xoff + 10						
				y = yoff-h/2-4							
														
				self.drawCanvas.text((x-2,y+2), 
					text = 'O', 
					fill= 'black', 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = 'O', 
					fill = mana[2], 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = mana[1], 
					fill = 'black', 
					font = fnt_mana)		
														
			if mana[0] == 1: #if Phyrexian mana 		
				w_letter, h = self.drawCanvas.textsize('o', 
					font = fnt_mana)					
																			
				xoff += w_letter + 4					
				x = self.X_RIGHT - xoff + 10				
				y = yoff-h/2							
														
				self.drawCanvas.text((x-2,y+2), 
					text = "o", 
					fill = 'black', 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = "o", 
					fill = mana[2], 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = mana[1], 
					fill='black', 
					font = fnt_mana)		
														
			if mana[0] == 2: #if split mana 			
				w_letter, h = self.drawCanvas.textsize('o', 
					font = fnt_mana)					
																			
				xoff += w_letter + 4						
				x = self.X_RIGHT - xoff + 10					
				y = yoff-h/2							
														
				self.drawCanvas.text((x-2,y+2), 
					text = "o", 
					fill = 'black', 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = "o", 
					fill = mana[2], 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = "/", 
					fill = mana[3], 
					font = fnt_mana)		
				self.drawCanvas.text((x,y), 
					text = mana[1], 
					fill = 'black', 
					font = fnt_mana)		
														
			i -= 1	

	def drawTypeline(self):
		(x1,y1) = (self.OFFSET*2, self.HEIGHT-90)
		(x2,y2) = (self.WIDTH-self.OFFSET*2, self.HEIGHT-50)
		#(x1,y1) = (self.LEFT+self.OFFSET*2, self.HEIGHT-90)
		#(x2,y2) = (self.RIGHT-self.OFFSET*2, self.HEIGHT-50)
		radius = 17

		if self.faceSide == 'normal':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')

			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= 'white', fillRight= 'white')
		elif self.faceSide == 'left':
			inc = 8
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')
			x2 = self.WIDTH/2 - 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= 'white', fillRight= 'white')			
		elif self.faceSide == 'right':
			x1 = self.WIDTH/2 + 4
			inc = 0
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= 'white', fillRight= 'white')	

		trash, h = self.drawCanvas.textsize(self.typeline, font=fnt_Bel_sm)
		yoff = y1+(y2-y1)/2
		x = self.X_LEFT-10
		y = yoff-h/2-2
		self.drawCanvas.text((x,y), 
			text = self.typeline, 
			fill='black', 
			font = fnt_Bel_sm)

		if 'Creature' in self.typeline:
			self.drawPowerToughness()	
		if 'Planeswalker' in self.typeline:
			self.drawLoyalty()

	def drawPowerToughness(self):
		#self.drawLevelPT(position = 2, powerToughness = "3/3")

		if self.layout == 'leveler':
			self.drawLevelPT(1,self.powerToughness)
		else:
			(x1,y1) = (self.RIGHT-145, self.HEIGHT-95)							#
			(x2,y2) = (self.RIGHT-self.OFFSET*2, self.HEIGHT-45)						#
			radius = 10

			#Draw Black Outline										#
			inc = 8
			#inc = 13													#
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')					#
																	#
			#Draw White Fill
			inc = 0	
			#inc = 5												#
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= 'white', fillRight= 'white')						#
																	#																#
			w, h = self.drawCanvas.textsize(self.powerToughness, 
				font = fnt_Bel_lg)

			xoff = x1 + (x2-x1)/2		
			yoff = y1 + (y2-y1)/2 - 5	
			x = xoff-w/2
			y = yoff-h/2

			self.drawCanvas.multiline_text((x, y), 
				text = self.powerToughness, 
				fill='black', 
				font = fnt_Bel_lg)

	def drawLevelPT(self,position,powerToughness):
			if position == 1:
				(x1,y1) = (self.RIGHT-145, 155)							#
				(x2,y2) = (self.RIGHT-self.OFFSET*2, 155+50)
			if position == 2:
				(x1,y1) = (self.RIGHT-145, 265)							#
				(x2,y2) = (self.RIGHT-self.OFFSET*2, 265+50)		
			elif position == 3:
				(x1,y1) = (self.RIGHT-145, 375)							#
				(x2,y2) = (self.RIGHT-self.OFFSET*2, 375+50)	

			radius = 10

			#Draw Black Outline										#
			inc = 8
			#inc = 13													#
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')					#
																	#
			#Draw White Fill
			inc = 0	
			#inc = 5												#
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= 'white', fillRight= 'white')						#
																	#																#
			w, h = self.drawCanvas.textsize(powerToughness, 
				font = fnt_Bel_lg)

			xoff = x1 + (x2-x1)/2		
			yoff = y1 + (y2-y1)/2 - 5	
			x = xoff-w/2
			y = yoff-h/2

			self.drawCanvas.multiline_text((x, y), 
				text = powerToughness, 
				fill='black', 
				font = fnt_Bel_lg)
	def drawLevelBox(self,position,level):
			if position == 2:
				(x1,y1) = (self.OFFSET*2, 265-45)							#
				(x2,y2) = (125, 265+5)		
			elif position == 3:
				(x1,y1) = (self.OFFSET*2, 375-45)							#
				(x2,y2) = (125, 375+5)	

			radius = 10

			#Draw Black Outline										#
			inc = 8
			#inc = 13													#
			round_rectangle2(canvas = self.drawCanvas, 
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc), 
				radius = radius+inc/2, 
				fillLeft= 'black', fillRight= 'black')					#
																	#
			#Draw White Fill
			inc = 0	
			#inc = 5												#
			round_rectangle2(canvas = self.drawCanvas,
				point1 = (x1-inc, y1-inc), 
				point2 = (x2+inc, y2+inc),  
				radius = radius+inc/2, 
				fillLeft= 'white', fillRight= 'white')	

			w, h = self.drawCanvas.textsize("LEVEL", 
				font = fnt_Bel_sm)

			xoff = x1 + (x2-x1)/2		
			yoff = y1 + (y2-y1)/2 - 5	
			x = xoff-w/2
			y = yoff-h/2-10
											#
			self.drawCanvas.multiline_text((x, y), 
				text = "LEVEL", 
				fill='black', 
				font = fnt_Bel_sm)																	#																#
			
			w, h = self.drawCanvas.textsize(level, 
				font = fnt_Bel_sm)

			xoff = x1 + (x2-x1)/2		
			yoff = y1 + (y2-y1)/2 - 5	
			x = xoff-w/2
			y = yoff-h/2+10

			self.drawCanvas.multiline_text((x, y), 
				text = level, 
				fill='black', 
				font = fnt_Bel_sm)

	def drawLoyalty(self):
		(x1,y1) = (self.WIDTH-100, self.HEIGHT-95)							#
		(x2,y2) = (self.WIDTH-self.OFFSET*2, self.HEIGHT-45)						#
		radius = 10

		#Draw Black Outline										#
		inc = 8
		#inc = 13													#
		round_rectangle2(canvas = self.drawCanvas, 
			point1 = (x1-inc, y1-inc), 
			point2 = (x2+inc, y2+inc), 
			radius = radius+inc/2, 
			fillLeft= 'black', fillRight= 'black')						#
																#
		#Draw White Fill
		inc = 0	
		#inc = 5												#
		round_rectangle2(canvas = self.drawCanvas,
			point1 = (x1-inc, y1-inc), 
			point2 = (x2+inc, y2+inc),  
			radius = radius+inc/2, 
			fillLeft= 'white', fillRight= 'white')							#		

		w, h = self.drawCanvas.textsize(self.loyalty,
			font = fnt_Bel_lg)#
		xoff = x1 + (x2-x1)/2							#		
		yoff = y1 + (y2-y1)/2 - 5						#
		x = xoff-w/2
		y = yoff-h/2						#
		self.drawCanvas.multiline_text((x,y), 
			text = self.loyalty, 
			fill='black', 
			font = fnt_Bel_lg)	


	def drawNormalText(self, word):
		w, trash = self.drawCanvas.textsize(
			text = word, 
			font = self.font)
		if self.layout == 'leveler':
			if (self.X_LEFT+self.xoff+w +40>= self.X_RIGHT):								
				self.yoff += self.h 											
				self.xoff = 0											
				if (self.bullets): 										
					self.xoff = 20 	
		else:
			if (self.X_LEFT+self.xoff+w -55>= self.X_RIGHT):								
				self.yoff += self.h 											
				self.xoff = 0											
				if (self.bullets): 										
					self.xoff = 20 	


		x = self.X_LEFT + self.xoff 								
		y = self.Y_TEXT + self.yoff 

		self.drawCanvas.text((x, y), 
			text = word, 
			font = self.font, 
			fill = 'Black')

		self.xoff += w-1			

	def drawWatermark(self):
		i = 0
		j = 0
		w, h = self.drawCanvas.textsize('G', 
				font = fnt_mana_huge)		
		for symbols in self.colorID:
			i += 1

		for symbols in self.colorID:
			if i == 1:
				if self.name == "Wastes":
					mana = manaCipher["C"]
				else:
					mana = manaCipher[self.colorID[0]]

				x = self.WIDTH/2 - w/2
				y = self.HEIGHT/2 - h/2 - 30

				if 'Basic' not in self.typeline:
					y = self.HEIGHT/2 - h/2 + 45
			elif i == 2:
				mana = manaCipher[self.colorID[j]]
				x = self.WIDTH/2 - w/2 - 130 + 260*j
				y = self.HEIGHT/2 - h/2 + 40
				j += 1

			self.drawCanvas.text((x-2 ,y+4), 
				text = mana[1], 
				fill = 'black', 
				font = fnt_mana_huge)
			self.drawCanvas.text((x,y), 
				text = mana[1], 
				fill = mana[3], 
				font = fnt_mana_huge)

	def drawLoyaltyAbility(self, word):
		if word[0] == "−":
			#replace with "-", drop the :
			word = "-" + word[1:]
		x = word.index(":")
		word = word[:x]

		w, trash = self.drawCanvas.textsize(
			text = word, 
			font = fnt_Bel_sm) 																
		x = self.X_LEFT - w/2 - 30 							
		y = self.Y_TEXT + self.yoff 								

		(x1,y1) = (self.X_LEFT-52, y+2)							
		(x2,y2) = (self.X_LEFT-10, y+28)
		
		#Draw Black Outline	
		radius = 5
		inc = 6	
		round_rectangle2(
			canvas = self.drawCanvas, 
			point1 = (x1-inc, y1-inc), 
			point2 = (x2+inc, y2+inc), 
			radius = radius, 
			fillLeft= 'black', fillRight= 'black')

		#Draw White Fill
		inc = 0
		round_rectangle2(
			canvas = self.drawCanvas, 
			point1 = (x1-inc, y1-inc), 
			point2 = (x2+inc, y2+inc), 
			radius = radius, 
			fillLeft= 'white', fillRight= 'white')

		self.drawCanvas.text((x, y), 
			text = word, 
			font = fnt_Bel_sm, 
			fill = 'Black')
	
	#def drawLevel(self,levelText,cardText,PT):

	def drawManaSimple(self, mana):
		w_letter, h_letter = self.drawCanvas.textsize(
			text = 'O', 
			font = fnt_mana_sm)						
													
		x = self.X_LEFT + self.xoff 							
		y = self.Y_TEXT + self.yoff -4					
													
		self.drawCanvas.text((x-2,y+2), 
			text = 'O',
			fill = 'black', 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = 'O', 
			fill = mana[2], 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = mana[1], 
			fill = 'black', 
			font = fnt_mana_sm)		
																		
		self.xoff += w_letter + 2 
	def drawManaPhyrexian(self, mana):
		w_letter, h_letter = self.drawCanvas.textsize(
			text = 'o', 
			font = fnt_mana_sm)						
													
		x = self.X_LEFT + self.xoff + 4						
		y = self.Y_TEXT + self.yoff - 4					
													
		self.drawCanvas.text((x-2,y+2), 
			text = 'o', 
			fill = 'black', 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = 'o', 
			fill = mana[2], 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = mana[1], 
			fill = 'black', 
			font = fnt_mana_sm)		
													
		w_letter += 6								
		self.xoff += w_letter
	def drawManaSplit(self, mana):
		w_letter, h_letter = self.drawCanvas.textsize(
			text = 'o',
			font = fnt_mana_sm)						
																		
		x = self.X_LEFT + self.xoff + 4						
		y = self.Y_TEXT + self.yoff - 4					
													
		self.drawCanvas.text((x-2,y+2), 
			text = 'o',
			fill = 'black', 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = 'o', 
			fill = mana[2], 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = '/',
			fill = mana[3], 
			font = fnt_mana_sm)		
		self.drawCanvas.text((x,y), 
			text = mana[1],
			fill = 'black', 
			font = fnt_mana_sm)		
													
		w_letter += 6								
		self.xoff += w_letter 
	def drawManaOther(self, mana):
		w_letter, h_letter = self.drawCanvas.textsize(
			text = 'O',
			font = fnt_mana_sm)						
													
		x = self.X_LEFT + self.xoff					
		y = self.Y_TEXT + self.yoff						
													
		self.drawCanvas.text((x,y), 
			text = mana[1], 
			fill = 'black', 
			font = fnt_mana_sm)		
																		
		self.xoff += w_letter - 2										

	def processText (self, card_text):
		chars = []								#
												#
		for char in card_text:					#
			chars.append(char)					#
			if char == '\n':					#
				chars.pop(-1)					#
				chars.append(' ')				#
				chars.append('\n')				#
				chars.append(' ')				#
												#
		card_text = []							#
		word = ""								#
												#
		for char in chars:						#
			if char == ' ':						#
				card_text.append(word)			#
				word = ""						#
			else:
				word = word + char				#
		card_text.append(word)					#

		#print(card_text)
		return card_text

class CARD:

	WIDTH = 750
	HEIGHT = 525 
	OFFSET = 20

	X_LEFT = 65				#limit_left = 65
	X_RIGHT = WIDTH - 110	#limit_right = width - 110

	Y_NAME = 50 			#offset_name_y = 50
	Y_TEXT = 110 			#offset_text_y = 110
	Y_TYPE = HEIGHT - 95  	#offset_type_y = height - 95  #440

	appendix = set()	

	#(side,board,deck_name,card)
	def __init__(self, side, board, deckName, cardName):
		self.side = side
		self.board = board
		self.deckName = deckName

		self.card = cardSearch(cardName) #card is a dictionary

		self.layout = self.card['layout']

		self.xoff = 0
		self.yoff = 0
		self.bullets = False												
		self.italics = False												
		self.font = fnt_Bel_sm

		'''
		if self.layout == 'transform':
			side1 = self.card['card_faces'][0]['name']
			side2 = self.card['card_faces'][1]['name']
			self.appendix.add((side1, side2))
		'''

	def printInfo(self):
		#		print("Layout: ", 			self.layout)
		#		print("Name: ",				self.name)
		#		print("Mana Cost: ",		self.manaCost)
		#		print("Color: ",			self.color)
		#		print("Color Identity: ",	self.colorID)
		#		print("Typeline: ",			self.typeline)
		#		print("Text: ",				self.text)
		#
		#		if 'Creature' in self.typeline:
		#			print("Power/Toughness: ", 		self.powerToughness)
		#		if 'Planeswalker' in self.typeline:
		#			print("Planeswalker loyalty: ", self.loyalty)
		#		
		#		print("Colortype: ",		self.colorType)
		#		print("Card Side: ",		self.side)
		#		print("Board: ",			self.board)
		#		print("Deckname: ",			self.deckName)

		self.canvas.show()

	def createCanvas(self):
		if self.side == 'A':
			self.canvas = Image.new('RGBA', 
				(self.WIDTH, self.HEIGHT), 'black')
			self.drawCanvas = ImageDraw.Draw(self.canvas)
			self.drawCanvas.rectangle(
				(2,0,self.WIDTH-2,self.HEIGHT-2), 
				fill = 'white')
		else:
			self.canvas = Image.new('RGBA', 
				(self.WIDTH, self.HEIGHT), 'white')
			self.drawCanvas = ImageDraw.Draw(self.canvas)
			self.drawCanvas.rectangle(
				(2,0,self.WIDTH-2,self.HEIGHT-2), 
				fill = 'black')

	def drawDeckname(self):
		if self.side == 'A':									#
			fill = 'black'								#
		else:											#
			fill='white'								#
		self.drawCanvas.text(
			(self.X_LEFT, self.HEIGHT - self.OFFSET*2 ), 
			text = 'Side ' + self.side +': ' + self.deckName, 
			fill = fill, 
			font = fnt_Bel_sm)				#

	def createImage(self):
		self.createCanvas()
		self.drawDeckname()

		if self.layout in ('normal','leveler'):
			#only one face
			normal = FACE(
				faceSide = 'normal',
				canvas = self.canvas,
				drawCanvas = self.drawCanvas,
				parentDict = self.card,
				cardDict = self.card)
			normal.createImage()
		elif self.layout == 'split':
			#two faces
			left = FACE(
				faceSide = 'left',
				canvas = self.canvas,
				drawCanvas = self.drawCanvas,
				parentDict = self.card,
				cardDict = self.card['card_faces'][0])
			#left.createImage()

			right = FACE(
				faceSide = 'right',
				canvas = self.canvas,
				drawCanvas = self.drawCanvas,
				parentDict = self.card,
				cardDict = self.card['card_faces'][1])
			#right.createImage()	

			left.coloredBorder()
			right.coloredBorder()

			left.drawTextBox()
			right.drawTextBox()

			left.drawNameline()
			right.drawNameline()

			left.drawTypeline()
			right.drawTypeline()

			left.drawText()
			right.drawText()
		elif self.layout in ('transform','flip'):
			normal = FACE(
				faceSide = 'normal',
				canvas = self.canvas,
				drawCanvas = self.drawCanvas,
				parentDict = self.card,
				cardDict = self.card['card_faces'][0])
				#cardDict = self.card['card_faces'][1])
			normal.createImage()
			#add to appendix
		elif self.layout == 'meld':
			#only one face
			normal = FACE(
				faceSide = 'normal',
				canvas = self.canvas,
				drawCanvas = self.drawCanvas,
				parentDict = self.card,
				cardDict = self.card)
			normal.createImage()
			#add card['all_parts'][1]['name'] to appendix
		#self.printInfo()

		#elif layout == 'transform':
			#one face, but print an additional card

		return self.canvas



def createProxy(board, deck1_name, card1_name, deck2_name, card2_name): #Recieves card names
	width = 750
	height = 525 
	fullCard = Image.new('RGBA', (width, height*2), 'black')
	
	if board == 'appA':
		card1 = CARD(side = "A", 
		board = board, 
		deckName = deck1_name,
		cardName = card1_name)

		card2 = CARD(side = "A", 
		board = board, 
		deckName = deck2_name,
		cardName = card2_name)
	elif board == 'appB':	
		card1 = CARD(side = "B", 
		board = board, 
		deckName = deck1_name,
		cardName = card1_name)

		card2 = CARD(side = "B", 
		board = board, 
		deckName = deck2_name,
		cardName = card2_name)
	else: #board == side or main
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
	elif 'app' in board:
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

# If the guantlet is called, it will generate a FACE image for every possible type of card
def gauntlet():
	names = [
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
		#"Faithful Squire // Kaiso, Memory of Loyalty", #Test: flip creature **Do not need full name

		"Bonfire of the Damned",	#Test: miracle card
		#"Start // Finish",			#Test: aftermath split card
		#"Wear // Tear",				#Test: fuse split card
		#"Triumph of Gerard",		#Test: Saga card 		***

		"Tarmogoyf",				#Test: * in power/toughness
		"Walking Ballista",			#Test: x cost, 0/0 creature
		"Nicol Bolas, God-Pharaoh",	#Test: SO MUCH TEXT, also planeswalker
		"Gideon, Ally of Zendikar",	#Test: planeswalker with a +, -, and 0

		"Tasigur, the Golden Fang",	#Test: split mana in card text, split mana next to normal mana
		"Vault Skirge",				#Test: phyrexian mana in cost and card text
		"Boros Reckoner",			#Test: color/color split mana in mana cost
		"Reaper King",				#Test: color/2 split mana cost and card text

		#"blah",						#Test: invalid card name
		]
	for cardName in names:
		CARD(side = "A", 
			board = "main", 
			deckName = "Deckname guantlet test",
			cardName = cardName).createImage().save(cardName+".png")#.show()

createProxy("side","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge").show()


#gauntlet()


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
			
	'''
	singleCard = {"board": "main",
			"deckNameA": nameA,
			"cardA": cardA,
			"deckNameB": nameB,
			"cardB": cardB}
	'''

	#self.card = cardSearch(cardName) #card is a dictionary

	#self.layout = self.card['layout']

	'''
	def processList(self):
		
	'''

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

	WIDTH = 750
	HEIGHT = 525 #1050
	offset = 20

	limit_left = 65
	limit_right = width - 110

	offset_name_y = 50
	offset_text_y = 110
	offset_type_y = height - 95  #440

	 fdfd 
	
	with is:split (split cards), 
	is:flip (flip cards), 
	is:transform (cards that transform), 
	is:meld (cards that meld), 
	and is:leveler (cards with Level Up)

	##Outside of Class
	card.print()

	##Inside Menu Class
	

	##Inside of Class

	#create proxy
	create card 1
	create card 2
	join cards on new canvas
	return full card proxy

	#Determine base
	if card.layout == "normal"
		card.print()

	elif card.layout == "split"

	elif card.layout == "flip" #aka kamigawa flip

	elif card.layout == "meld" #ahhhhhhh

	elif card.layout == "leveler"
	

	cardSearch(card_name)
		return card_dictionary

	createProxy(board, deck1_name, card1_name, deck2_name, card2_name)
		cardSearch(card1_name)
		createImage("B",board,deck1_name,card1).rotate(180)
		join two sides
		return fullCard

	round_rectangle2(canvas, point1, point2, radius, fill1, fill2)
		draw box


	createImage(side,board,deck_name,card)
		

		for each card segment
			create canvas + border
			create color border
			create name bar
				print name
				print mana cost
			create type bar
				print type
				if creature but not leveler
					print power/toughness
				if planeswalker
					print loyalty
			create text box
				process card text
				print text
					for word in card text
						if leveler, print p/t for each level
						if planeswalker, print loyalty for each ability
						if saga, print segments
						if mana
							print prefix normally
							if normal
								print normal mana
							elif phyrexian
								print phyrexian mana
							elif split
								print split mana
							elif other
								print other, i.e. energy
							print postfix normally


		if basic land
			create watermark
		draw deck name
		return blank_image
	

	submitButton (event)
		combineLists(deckname1,main1,side1,deckname2,main2,side2)
			expandList(decklist)
				return expandedList
			return combinedList

		createPDF(proxyList)
			for each position
				createProxy(board, 
					deck1_name, card1_name, 
					deck2_name, card2_name)
				place proxy
			PDF.save()


''' 