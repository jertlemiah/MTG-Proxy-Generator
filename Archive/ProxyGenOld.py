from PIL import Image, ImageDraw, ImageFont
import textwrap
from math import atan2
import requests
import json
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image 
#from reportlab.platypus import Image
from reportlab.pdfgen import canvas as canvas2
from reportlab.lib.units import inch

#_____Colors_____
	#White
color_w = '#CACCC8' #rgb(202,204,200)
color_wMana = '#FCFCC1' #rgb(252,252,193)

	#Blue
color_u = '#127CAC' #rgb(18,124,172)
color_uMana = '#67C1F5' #rgb(103,193,245)

	#Black
color_b = '#363732' #rgb(54,55,50)
color_bMana = '#848484' #rgb(132,132,132)

	#Red
color_r = '#D85950' #rgb(216,89,80)
color_rMana = '#F85555' #rgb(248,85,85)
cr_pale =  '#D8857F' #rgb(216,133,12)

	#Green
color_g = '#1F7751' #rgb(31, 119,81)
#cg_mana = '#26B569' #rgb(38,181,105)
color_gMana = '#90C3A1' #rgb(144,195,161)

	#Colorless
color_cMana = '#CCC2C0' #rgb(204,194,192)

#"Gold" Card
cgold = '#D5C089' #rgb(213,192,137)
#cgold = '#B99B5F' #rgb(213,175,80)

#_____fonts______________________________________
fnt_Bel_lg = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",35)
fnt_Bel_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",27)
fnt_italic = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MPLANTINIT.TTF",30)
fnt_magic = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MAGICSYMBOLS2008.TTF",45)
fnt_magic_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MAGICSYMBOLS2008.TTF",40)

fnt_mana = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",44)
fnt_mana_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",34)
fnt_mana_med = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",70)
fnt_mana_big = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",100)
fnt_mana_big2 = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",130)
fnt_mana_big3 = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016_new2.TTF",115)
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


#_____Various Variables_____
width = 750
height = 525 #1050
offset = 20

limit_left = 65
limit_right = width - 110

offset_name_y = 50
offset_text_y = 110
offset_type_y = height - 95  #440

#__Sample Decks___________________________________
sample_nameA = "Bant Spirits"

sample_mainA = ("2 Anafenza, Kin-Tree Spirit"
	+ "\n1 Birds of Paradise"
	+ "\n2 Breeding Pool"
	+ "\n2 Cavern of Souls"
	+ "\n4 Collected Company"
	+ "\n4 Drogskol Captain"
	+ "\n3 Flooded Strand"
	+ "\n1 Forest"
	+ "\n1 Gavony Township"
	+ "\n1 Hallowed Fountain"
	+ "\n1 Island"
	+ "\n1 Kira, Great Glass-Spinner"
	+ "\n4 Mausoleum Wanderer"
	+ "\n4 Misty Rainforest"
	+ "\n4 Noble Hierarch"
	+ "\n2 Path to Exile"
	+ "\n1 Plains"
	+ "\n4 Rattlechains"
	+ "\n1 Razorverge Thicket"
	+ "\n2 Seachrome Coast"
	+ "\n4 Selfless Spirit"
	+ "\n4 Spell Queller"
	+ "\n3 Supreme Phantom"
	+ "\n1 Temple Garden"
	+ "\n3 Windswept Heath")

sample_sideA = ("2 Engineered Explosives"
	+ "\n1 Kira, Great Glass-Spinner"
	+ "\n2 Negate"
	+ "\n2 Path to Exile"
	+ "\n2 Qasali Pridemage"
	+ "\n3 Rest in Peace"
	+ "\n3 Stony Silence")

sample_nameB = "BR Hollow One"

sample_mainB = ("3 Blackcleave Cliffs"
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
	+ "\n2 Wooded Foothills")

sample_sideB = ("2 Ancient Grudge"
	+ "\n2 Engineered Explosives"
	+ "\n3 Fatal Push"
	+ "\n3 Grim Lavamancer"
	+ "\n3 Leyline of the Void"
	+ "\n2 Thoughtseize")


def cardSearch(card_name):
    url = 'https://api.scryfall.com/cards/named?exact=!"'	#Base URL
    card_name = card_name.replace(' ', '%20')				#Replace spaces
    final_url = url + card_name + '"'						#Final URL
    card_dictionary = requests.get(url=final_url).json()

    return card_dictionary

#THE MOST IMPORTANT FUNCTION CALL
def createProxy(board, deck1_name, card1_name, deck2_name, card2_name): #Recieves card names
	fullCard = Image.new('RGBA', (width, height*2), 'black')
	
	card1 = cardSearch(card1_name)
	card2 = cardSearch(card2_name)

	card1_image = createImage("B",board,deck1_name,card1).rotate(180)
	card2_image = createImage("A",board,deck2_name,card2)

	card1_area = (0,0,width,height)
	card2_area = (0,height,width,height*2)

	fullCard.paste(card1_image,card1_area)
	fullCard.paste(card2_image,card2_area)

	#fullCard.save("Full Card.png")

	#fullCard.show()
	return fullCard

 
def round_rectangle(canvas, point1, point2, radius, fill):
    """Draw a rounded rectangle"""
    x1, y1 = point1
    x2, y2 = point2
    canvas.ellipse((x1, y1, x1+radius * 2, y1+radius * 2), fill=fill)
    canvas.ellipse((x1, y2-radius * 2, x1+radius * 2, y2), fill=fill)
    canvas.ellipse((x2-radius*2, y1, x2, y1+radius * 2), fill=fill)
    canvas.ellipse((x2-radius*2, y2-radius * 2, x2, y2), fill=fill)
    canvas.rectangle(((x1,y1+radius),(x2,y2-radius)), fill = fill)
    canvas.rectangle(((x1+radius,y1),(x2-radius,y2)), fill = fill)

def round_rectangle2(canvas, point1, point2, radius, fill1, fill2):
    """Draw a rounded, two color rectangle"""
    x1, y1 = point1
    x2, y2 = point2
    xc = (x2-x1)/2

    canvas.ellipse((x1, y1, x1+radius * 2, y1+radius * 2), fill=fill1)
    canvas.ellipse((x1, y2-radius * 2, x1+radius * 2, y2), fill =fill1)
    canvas.rectangle(((x1,y1+radius),(xc,y2-radius)), fill = fill1)
    canvas.rectangle(((x1+radius,y1),(xc,y2)), fill = fill1)    

    canvas.ellipse((x2-radius*2, y1, x2, y1+radius * 2), fill=fill2)
    canvas.ellipse((x2-radius*2, y2-radius * 2, x2, y2), fill=fill2)
    canvas.rectangle(((xc,y1+radius),(x2,y2-radius)), fill = fill2)
    canvas.rectangle(((xc,y1),(x2-radius,y2)), fill = fill2)


def createImage(side,board,deck_name,card): #Receives card dictionary
	#_____Populate Card Info_____
	card_name = card['name']
	card_mana = card['mana_cost']
	card_color = card['colors']
	i = 0
	card_colorID = card['color_identity']
	card_type = card['type_line']
	card_text = card['oracle_text']
	if 'Creature' in card_type:
		card_pt = (card['power']+"/"+card['toughness'])
	if 'Planeswalker' in card_type:
		card_loyalty = card['loyalty']

	multicolor = False
	bicolor = False
	if 'Land' in card_type:
		for icon in card_colorID:
			i += 1
			if i == 2:
				bicolor = True
			elif i > 2:
				bicolor = False
				multicolor = True
	else:
		for icon in card_color:
			i += 1
			if i == 2:
				bicolor = True
			elif i > 2:
				bicolor = False
				multicolor = True

	#_____Create Image Canvas_____
	if side == 'A':
		blank_image = Image.new('RGBA', (width, height), 'black')
		img_draw = ImageDraw.Draw(blank_image)
		img_draw.rectangle((2,0,width-2,height-2),fill = 'white')
	else:
		blank_image = Image.new('RGBA', (width, height), 'white')
		img_draw = ImageDraw.Draw(blank_image)
		img_draw.rectangle((2,0,width-2,height-2),fill = 'black')

	#_____Colored Border_____
	pt1 = (offset-2,offset-5)
	pt2 = (width-offset+2,height-50)
	fill_mana = color_cMana
	fill_mana2 = color_cMana

	if (multicolor):
		fill_mana = cgold
	else:
		if 'W' in card_color:
				fill_mana = color_wMana
		if 'U' in card_color:
			if fill_mana == color_cMana:
				fill_mana = color_u
			else:
				fill_mana2 = color_u
		if 'B' in card_color:
			if fill_mana == color_cMana:
				fill_mana = color_b
			else:
				fill_mana2 = color_b
		if 'R' in card_color:
			if fill_mana == color_cMana:
				fill_mana = color_r
			else:
				fill_mana2 = color_r
		if 'G' in card_color:
			if fill_mana == color_cMana:
				fill_mana = color_g
			else:
				fill_mana2 = color_g
	if 'Land' in card_type:
		if 'W' in card_colorID or "Plains" in card_text:
				fill_mana = color_wMana
		if 'U' in card_colorID or "Island" in card_text:
			if fill_mana == color_cMana:
				fill_mana = color_u
			else:
				fill_mana2 = color_u
		if 'B' in card_colorID or "Swamp" in card_text:
			if fill_mana == color_cMana:
				fill_mana = color_b
			else:
				fill_mana2 = color_b
		if 'R' in card_colorID or "Mountain" in card_text:
			if fill_mana == color_cMana:
				fill_mana = color_r
			else:
				fill_mana2 = color_r
		if 'G' in card_colorID or "Forest" in card_text:
			if fill_mana == color_cMana:
				fill_mana = color_g
			else:
				fill_mana2 = color_g
	
	thick = 5
	round_rectangle(img_draw, 
		(pt1[0]-thick,pt1[1]-thick), 
		(pt2[0]+thick,pt2[1]+thick), 
		radius = 40, fill= 'black')

	if(bicolor or "Pay 1 life, Sacrifice" in card_text):
		round_rectangle2(canvas = img_draw, 
			point1 = pt1, 
			point2 = pt2, 
			radius = 40, 
			fill1 = fill_mana, 
			fill2 = fill_mana2)
	else:
		round_rectangle(img_draw, pt1, pt2, radius = 40, fill= fill_mana)

	#_____Rules Text Box_____
	pt1 = (offset*2,100-30)
	pt2 = (width-offset*2,height-100+20)

	inc = -2
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-10), 
		(pt2[0]+inc,pt2[1]+10), radius = 20+inc/2, fill= 'black')

	inc = -10
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]+35), 
		(pt2[0]+inc,pt2[1]-30), radius = 20+inc/2, fill= 'white')

	#_____Type Box_____ *height of this line is 32
	pt1 = (offset*2,height-100)
	pt2 = (width-offset*2,height-50)

	inc = 8
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc,pt2[1]+inc), radius = 20+inc/2, fill= 'black')

	inc = 0
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc , pt2[1]+inc), radius = 20+inc/2, fill= 'white')

	trash, h = img_draw.textsize(card_type, font=fnt_Bel_sm)
	yoff = pt1[1]+(pt2[1]-pt1[1])/2
	img_draw.text((limit_left-4, yoff-h/2), card_type, 
		fill='black', font = fnt_Bel_sm)


	#_____Power/Toughness_______________________________________#
	if 'Creature' in card_type:									#
		pt1 = (width-125,height-100)							#
		pt2 = (width-offset*2,height-50)						#
			
		#Draw Black Outline										#
		inc = 8													#
		round_rectangle(img_draw, 
			(pt1[0]-inc,pt1[1]-inc), 	
			(pt2[0]+inc,pt2[1]+inc), 
			radius = 20+inc/2, fill= 'black')					#
																#
		#Draw White Fill
		inc = 0													#
		round_rectangle(img_draw, 
			(pt1[0]-inc,pt1[1]-1), 
			(pt2[0]+inc,pt2[1]+1), 
			radius = 15, fill= 'white')							#
																#
		#pt1 = (width-150,height-100)							#
		#pt2 = (width-offset*2,height-55)						#
																#
		w, h = img_draw.textsize(card_pt,font = fnt_Bel_lg)		#
		yoff = pt1[1]+(pt2[1]-pt1[1])/2	- 5						#
		xoff = pt1[0]+(pt2[0]-pt1[0])/2							#
		img_draw.multiline_text((xoff-w/2,yoff-h/2), card_pt, 
			fill='black', font = fnt_Bel_lg)					#
	#_____END Power/Toughness___________________________________#

	#_____Planeswalker Loyalty___________
	if 'Planeswalker' in card_type:
		#"loyalty": "7"
#		pt1 = (width-125,height-100)							#
		pt1 = (width-100,height-100)							#
		pt2 = (width-offset*2,height-50)						#
			
		#Draw Black Outline										#
		inc = 8													#
		round_rectangle(img_draw, 
			(pt1[0]-inc,pt1[1]-inc), 	
			(pt2[0]+inc,pt2[1]+inc), 
			radius = 20+inc/2, fill= 'black')					#
																#
		#Draw White Fill
		inc = 0													#
		round_rectangle(img_draw, 
			(pt1[0]-inc,pt1[1]-1), 
			(pt2[0]+inc,pt2[1]+1), 
			radius = 15, fill= 'white')							#
																#
		#pt1 = (width-150,height-100)							#
		#pt2 = (width-offset*2,height-55)						#
#																#
#		w, h = img_draw.textsize("?",font = fnt_mana_big3)#
#		yoff = pt1[1]+(pt2[1]-pt1[1])/2	- 5						#
#		xoff = pt1[0]+(pt2[0]-pt1[0])/2							#
#		img_draw.multiline_text((xoff-w/2,yoff-h/2), "?", 
#			fill='black', font = fnt_mana_big3)					#

#		w, h = img_draw.textsize("?",font = fnt_mana_big2)#
#		yoff = pt1[1]+(pt2[1]-pt1[1])/2					#
#		xoff = pt1[0]+(pt2[0]-pt1[0])/2							#
#		img_draw.multiline_text((xoff-w/2,yoff-h/2), "?", 
#			fill='black', font = fnt_mana_big2)					#
#
#		w, h = img_draw.textsize("?",font = fnt_mana_big)#
#		yoff = pt1[1]+(pt2[1]-pt1[1])/2						#
#		xoff = pt1[0]+(pt2[0]-pt1[0])/2							#
#		img_draw.multiline_text((xoff-w/2-5,yoff-h/2+3), "?", 
#			fill='white', font = fnt_mana_big)					#		

		w, h = img_draw.textsize(card_loyalty,font = fnt_Bel_lg)#
		yoff = pt1[1]+(pt2[1]-pt1[1])/2	- 5						#
		xoff = pt1[0]+(pt2[0]-pt1[0])/2							#
		img_draw.multiline_text((xoff-w/2 ,yoff-h/2), card_loyalty, 
			fill='black', font = fnt_Bel_lg)					#
	#_____END Planeswalker Loyalty___________	

	#_____Basic Land Watermark______________
	if 'Basic Land' in card_type:
		if card_name == "Wastes":
			mana = manaCipher["C"]
		else:
			mana = manaCipher[card_colorID[0]]

		w, h = img_draw.textsize('G', font = fnt_mana_huge)

		x = width/2 - w/2
		y = height/2 - h/2

		img_draw.text((x-4,y+4), mana[1], fill='black', font = fnt_mana_huge)
		img_draw.text((x,y), mana[1], fill=mana[3], font = fnt_mana_huge)
	#_____END Basic Land Watermark______________

	#_____Card Name_________________________________________________
	pt1 = (offset*2,offset*2+5)
	pt2 = (width-offset*2,100-5)

	inc = 8
	round_rectangle(img_draw, 
		(pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc,pt2[1]+inc), 
		radius = 20, fill= 'black')

	inc = 0
	round_rectangle(img_draw, 
		(pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc,pt2[1]+inc),
		radius = 10, fill= 'white')

	trash, h = img_draw.textsize(card_name, font = fnt_magic)
	yoff = pt1[1]+(pt2[1]-pt1[1])/2	

	img_draw.text((limit_left, yoff-h/2+2), 
		card_name, fill='black', 
		font = fnt_Bel_lg)
	#_________________________________________________________________

	#_____Mana Cost_________________________________#
	yoff = pt1[1]+(pt2[1]-pt1[1])/2					#
	i=0												#
	xoff = -50										#
	mana = ""										#
	cost = []										#	
													#
	for char in card_mana:							#
		if char == '}':								#
			cost.append(mana)						#
			mana = ""								#
		elif char != '{':							#
			mana += char 							#
													#
	##print(cost)									#
													#
	i = -1											#
													#
	for blah in cost:								#
		mana = manaCipher[cost[i]]					#
													#
		if mana[0] == 0: #if simple mana 			#
			w_letter, h = img_draw.textsize('O', 
				font = fnt_mana)					#
													#
			w_letter += 2							#
			xoff += w_letter						#
			x = limit_right - xoff 					#	
			y = yoff-h/2-4							#
													#
			img_draw.text((x-2,y+2), "O", 
				fill='black', font = fnt_mana)		#
			img_draw.text((x,y), "O", 
				fill=mana[2], font = fnt_mana)		#
			img_draw.text((x,y), mana[1], 
				fill='black', font = fnt_mana)		#
													#
		if mana[0] == 1: #if Phyrexian mana 		#
			w_letter, h = img_draw.textsize('o', 
				font = fnt_mana)					#
													#
			w_letter += 4							#
			xoff += w_letter						#
			x = limit_right - xoff 					#
			y = yoff-h/2							#
													#
			img_draw.text((x-2,y+2), "o", 
				fill='black', font = fnt_mana)		#
			img_draw.text((x,y), "o", 
				fill=mana[2], font = fnt_mana)		#
			img_draw.text((x,y), mana[1], 
				fill='black', font = fnt_mana)		#
													#
		if mana[0] == 2: #if split mana 			#
			w_letter, h = img_draw.textsize('o', 
				font = fnt_mana)					#
													#
			w_letter += 4							#
			xoff += w_letter						#
			x = limit_right - xoff 					#
			y = yoff-h/2							#
													#
			img_draw.text((x-2,y+2), "o", 
				fill='black', font = fnt_mana)		#
			img_draw.text((x,y), "o", 
				fill=mana[2], font = fnt_mana)		#
			img_draw.text((x,y), "/", 
				fill=mana[3], font = fnt_mana)		#
			img_draw.text((x,y), mana[1], 
				fill='black', font = fnt_mana)		#
													#
		i -= 1										#
	#_____END Mana Cost_____________________________#

	##___PROCESSING CARD TEXT_______________#
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
	##print(card_text)						#
	#____END PROCESSING CARD TEX____________#

	#_____Card Text_____________________________________________#
	trash, h = img_draw.textsize("Sample for height reasons", 
		font=fnt_Bel_sm) #comes out to 37						#
																#
	h -= 4			#lowers h to 32 							#
	yoff = 0													#
	xoff = 0													#
	bullets = False												#
	italics = False												#
	normalFont = fnt_Bel_sm										#
																#
	for word in card_text:										#
		symbol = False											#
		if (word == '\n'):										#
			yoff += h + 5										#
			xoff = 0											#
			bullets = False										#
			if (word[0]=='•'):									#
				bullets = True 									#
			continue											#
		elif "(" in word: 										#
			italics = True 										#
			normalFont = fnt_italic	 							#
		#__Planeswalker Loyalty___
		if ":" in word and "Planeswalker" in card_type:
			if word[0] == "−":
				#replace with "-", drop the :
				word = "-" + word[1:]
			x = word.index(":")
			word = word[:x]

			#NEEDS BACKDROP
#			w, trash = img_draw.textsize("]", 
#				font=fnt_mana_med) 								#
#			x = limit_left-w 								#
#			y = offset_text_y+yoff 								#
#			img_draw.text((x, y), "]", 
#				font=fnt_mana_med, fill='black')			
#
#	fullCard = Image.new('RGBA', (width, height*2), 'black')
	
#	card1 = cardSearch(card1_name)
#	card2 = cardSearch(card2_name)

#	card1_image = createImage("B",board,deck1_name,card1).rotate(180)
#	card2_image = createImage("A",board,deck2_name,card2)

#	card1_area = (0,0,width,height)
#	card2_area = (0,height,width,height*2)

#	fullCard.paste(card1_image,card1_area)
#	fullCard.paste(card2_image,card2_area)
			
#			loyalty_up = Image.open("L_naut.png")
#			loyalty_up = loyalty_up.resize((150,90))
#			area = (0,0,150,90)
#
#			blank_image.paste(loyalty_up,area)			
#
			w, trash = img_draw.textsize(word, 
				font=normalFont) 								#
#			x = limit_left-w - 10 								#
			x = limit_left-w/2 - 27 								#
			y = offset_text_y+yoff 								#

			pt1 = (limit_left-52,y+2)							#
			pt2 = (limit_left-5,y+28)						#
			
			#Draw Black Outline										#
			inc = 6													#
			round_rectangle(img_draw, 
				(pt1[0]-inc,pt1[1]-inc), 	
				(pt2[0]+inc,pt2[1]+inc), 
				radius = 5, fill= 'black')					#
																	#
			#Draw White Fill
			inc = 0													#
			round_rectangle(img_draw, 
				(pt1[0]-inc,pt1[1]-1), 
				(pt2[0]+inc,pt2[1]+1), 
				radius = 5, fill= 'white')							#

			img_draw.text((x, y), word, 
				font=normalFont, fill='Black')
			#+1: D
			#.\n−2: E
			word = "" #Stops the last bit from printing 
																#
		#__If mana symbol__										#
		if "{" in word:											#
			begin = ""											#
			end = ""											#
													#
			#__Saving the non-mana bits__ 						#
			#print("Before" + word)								#
			x = word.index("{")									#
			begin = word[:x]									#
			word = word[x:]										#
			#print("Mid" + word)									#
			reverse = ""										#
			for char in word: 									#
				reverse = char + reverse 						#
			x = reverse.index("}")								#
			if(x!=0):											#
				end = word[-(x):]								#
				word = word[:-x]								#
			#print("End" + word)									#
																#
			#__Parsing the mana bits__ 							#
			mana = ""											#
			cost = []											#	
			for char in word:									#
				if char == '}':									#
					cost.append(mana)							#
					mana = ""									#
				elif char != '{':								#
					mana += char 								#
			#i = 0												#
			#print(cost) 										#
																#
			#__Printing the beginning__							#
			word = begin 										#
			w, trash = img_draw.textsize(word, 
				font=normalFont) 								#
			x = limit_left+xoff 								#
			y = offset_text_y+yoff 								#
			img_draw.text((x, y), word, 
				font=normalFont, fill='Black')					#
			xoff += w-1											#
																#			
			#__Printing the mana__								#
			for mana in cost:									#
				mana = manaCipher[mana]							#
																#
				#If simple mana									#
				if mana[0] == 0:  								#
					w_letter, h_letter = img_draw.textsize('O', 
						font = fnt_mana_sm)						#
																#
					x = limit_left + xoff 						#	
					y = offset_text_y+yoff -4					#
																#
					img_draw.text((x-2,y+2), "O",
						fill='black', font = fnt_mana_sm)		#
					img_draw.text((x,y), "O", 
						fill=mana[2], font = fnt_mana_sm)		#
					img_draw.text((x,y), mana[1], 
						fill='black', font = fnt_mana_sm)		#
																#					
					xoff += w_letter + 2						#
																#				
				#If Phyrexian mana								#
				if mana[0] == 1:  								#
					w_letter, h_letter = img_draw.textsize('o', 
						font = fnt_mana_sm)						#
																#
					x = limit_left + xoff + 4					#	
					y = offset_text_y+yoff - 4					#
																#
					img_draw.text((x-2,y+2), "o", 
						fill='black', font = fnt_mana_sm)		#
					img_draw.text((x,y), "o", 
						fill=mana[2], font = fnt_mana_sm)		#
					img_draw.text((x,y), mana[1], 
						fill='black', font = fnt_mana_sm)		#
																#
					w_letter += 6								#
					xoff += w_letter							#
																#
				#If split mana 									#
				if mana[0] == 2: 								#
					w_letter, h_letter = img_draw.textsize('o',
						font = fnt_mana_sm)						#
																#
																#
					x = limit_left + xoff + 4					#	
					y = offset_text_y+yoff -4					#
																#
					img_draw.text((x-2,y+2), "o",
						fill='black', font = fnt_mana_sm)		#
					img_draw.text((x,y), "o", 
						fill=mana[2], font = fnt_mana_sm)		#
					img_draw.text((x,y), "/",
						fill=mana[3], font = fnt_mana_sm)		#
					img_draw.text((x,y), mana[1],
						fill='black', font = fnt_mana_sm)		#
																#
					w_letter += 6								#
					xoff += w_letter 							#
																#
				#If other, i.e. energy							#
				if mana[0] == 3:		 						#
					w_letter, h_letter = img_draw.textsize('O', 
						font = fnt_mana_sm)						#
																#
					x = limit_left + xoff 						#	
					y = offset_text_y+yoff 						
																#
					img_draw.text((x,y), mana[1], 
						fill='black', font = fnt_mana_sm)		#
																#					
					xoff += w_letter - 2						#				
																#
			word = end 											#
 																#
		#__Printing if not mana/ printing the ending__			#
		w, trash = img_draw.textsize(word + ' ', 
			font=normalFont)									#
																#
		if (xoff+w >= limit_right):								#
			yoff += h 											#
			xoff = 0											#
			if (bullets): 										#
				xoff = 20										#
																#
		x = limit_left+xoff 									#
		y = offset_text_y+yoff 									#
																#
		img_draw.text((x, y), 
			word + ' ', font=normalFont, fill='Black')			#
																#	
		xoff += w-1												#
																#
		#__Check for end of italics__							#
		if (')' in word):										#
			italics = False										#
			normalFont = fnt_Bel_sm								#
																#
	#_____END Card Text_________________________________________#
		
	#card.draw_deckName()	
	#_____Deck Name_________________________________#
	if side == 'A':									#
		fill = 'black'								#
	else:											#
		fill='white'								#
	img_draw.text((limit_left,height - offset*2 ), 
		'Side ' + side +': ' + deck_name, 
		fill = fill, font = fnt_Bel_sm)				#
	#_____Deck Name_________________________________#


	blank_image.save('drawn_image.png')
	#blank_image.show()
	return blank_image

#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
#createProxy("Tasigur, the Golden Fang", "Splinter Twin", "Vault Skirge", "Junk")
#createProxy("Boros Reckoner", "Splinter Twin", "Reaper King", "Junk")
#createProxy("Island", "Splinter Twin", "Aether Hub", "Junk")

def createPDF(proxyList):
	#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
	c = canvas2.Canvas("Proxies.pdf")
	c.setPageSize((8.5*inch,11*inch))

	card_x = 2.5
	card_y = 3.5

	margin_x = 0.5
	margin_y = 0.25

#	n = 0
#	board = proxyList[n][0] 
#	deck1_name = proxyList[n][1]
#	card1_name = proxyList[n][2]
#	deck2_name = proxyList[n][3]
#	card2_name = proxyList[n][4] 

	#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
#	cardImage = createProxy(board, 
#		deck1_name, card1_name, 
#		deck2_name, card2_name)


	#	proxyListImg = []
#
#	for card in proxylist:
#		board = card[0] 
#		deck1_name = card[1]
#		card1_name = card[2]
#		deck2_name = card[3]
#		card2_name = card[4] 
#
#		proxyListImg.append(createProxy(board, 
#			deck1_name, card1_name, 
#			deck2_name, card2_name))


	#(x,y) is bottom left corner
	for k in range(0,9):
		for i in range(0,3):
			for j  in range(0,3):
				x = margin_x + 0 + card_x*i
				y = margin_y + 0 + card_y*j
				n = j+i*3+k*9

				if n >= 75:
					break

				board = proxyList[n][0] 
				deck1_name = proxyList[n][1]
				card1_name = proxyList[n][2]
				deck2_name = proxyList[n][3]
				card2_name = proxyList[n][4] 

				cardImage = createProxy(board, 
					deck1_name, card1_name, 
					deck2_name, card2_name)
				c.drawInlineImage(cardImage, x*inch,y*inch, 
					(card_x)*inch, (card_y)*inch)
		c.showPage()

	#c.showPage() ends the current page and goes to the next one

	#c.showPage()
	c.save()
#createPDF()

def expandList(decklist):
	i = 0
	decklist = decklist.split('\n')
	decklist.pop(-1)

	expandedList = []

	for card in decklist:
		i = card.index(' ')
		n = int(card[:i])
		name = card[i+1:]
		while n>0:
			expandedList.append(name)
			n -= 1

	return expandedList

def combineLists(deckname1,main1,side1,deckname2,main2,side2):
	i = 0
	combinedList = []

	main1 = expandList(main1)
	side1 = expandList(side1)
	
	main2 = expandList(main2)
	side2 = expandList(side2)

	for cards in main1:
		singleCard = ("main",deckname1,main1[i],deckname2,main2[i])
		combinedList.append(singleCard)
		i += 1
	i=0
	for cards in side1:
		singleCard = ("side",deckname1,side1[i],deckname2,side2[i])
		combinedList.append(singleCard)
		i += 1
	return combinedList

def submitButton (event):
	#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
	deckA = name_A.get()
	deckB = name_B.get()

	mainA = main_A.get(1.0, END)
	mainB = main_B.get(1.0, END)

	sideA = side_A.get(1.0,END)
	sideB = side_B.get(1.0,END)

	#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")

	proxyList = combineLists(deckA,mainA,sideA,deckB,mainB,sideB)
	#returns (board,deckname1,card1name,deckname2,card2name)

#	proxyListImg = []
#
#	for card in proxylist:
#		board = card[0] 
#		deck1_name = card[1]
#		card1_name = card[2]
#		deck2_name = card[3]
#		card2_name = card[4] 
#
#		proxyListImg.append(createProxy(board, 
#			deck1_name, card1_name, 
#			deck2_name, card2_name))

	createPDF(proxyList)	
	print("DONE!")
	#createPDF(proxyListImg)	
	#print(proxylist)

#createProxy("main","Splinter Twin","Plains","Junk","Forest")
#createProxy("main","Splinter Twin","Mountain","Junk","Island")
#createProxy("main","Splinter Twin","Swamp","Junk","Ugin, the Spirit Dragon")
#createProxy("main","Splinter Twin","Steam Vents","Junk","Zealous Persecution").show()
#createProxy("main","Splinter Twin","Reaper King","Junk","Chandra, Torch of Defiance").show()
#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge").show()
createProxy("main","Splinter Twin","Nicol Bolas, God-Pharaoh","Junk","Gideon, Ally of Zendikar").show()
createProxy("main","Splinter Twin","Driven // Despair","Junk","Triumph of Gerard").show()

#def createMenu():
tk = Tk()
menuWidth = 75*3
menuHeight = 105*3
canvas = Canvas(tk,width = menuWidth, height = menuHeight)
canvas.grid(row = 4, column = 6)
img = ImageTk.PhotoImage(Image.open("Full Card.png"))
canvas.create_image(0,0,anchor=NW,image = img)

#__________DECK A__________#
col = 1
#Deck Name
Label(tk, text='Deck A:').grid(row=1, column=col, sticky=NSEW, padx = 20)
name_A = Entry(tk)
name_A.grid(row=2, column=col, sticky=NSEW, padx = 20)
name_A.insert(END,sample_nameA)
name_A.config(width = 35)

#Mainboard Content
Label(tk, text='Mainboard:').grid(row=3, column=col, sticky=NSEW, padx = 20)

scroll_mainA = Scrollbar(tk)
scroll_mainA.grid(row=4, column=col+1, sticky=NSEW)

main_A = Text(tk, yscrollcommand=scroll_mainA.set)
main_A.grid(row=4, column=col, sticky=NSEW)
main_A.insert(END,sample_mainA)
main_A.config(width = 35, height = 20)

#Sideboard Contect
Label(tk, text='Sideboard:').grid(row=5, column=col, sticky=NSEW, 
	padx = 20)
side_A = Text(tk)
side_A.grid(row=6, column=col, sticky=NSEW, padx = 20)
side_A.insert(END,sample_sideA)
side_A.config(width = 35, height = 10)
#__________________________

#__________DECK B__________#
col = 3
#Deck Name
Label(tk, text='Deck B:').grid(row=1, column=col, sticky=NSEW, padx = 20)
name_B = Entry(tk)
name_B.grid(row=2, column=col, sticky=NSEW, padx = 20)
name_B.insert(END,sample_nameB)
name_B.config(width = 35)

#Mainboard Content
Label(tk, text='Mainboard:').grid(row=3, column=col, sticky=NSEW)

scroll_mainB = Scrollbar(tk)
scroll_mainB.grid(row=4, column=col, sticky=NSEW, padx = 20)
scroll_mainB.config(width = 5)

main_B = Text(tk, yscrollcommand=scroll_mainB)
main_B.grid(row=4, column=col, sticky=NSEW, padx = 20)
main_B.insert(END,sample_mainB)
main_B.config(width = 35, height = 20)

#Sideboard Contect
Label(tk, text='Sideboard:').grid(row=5, column=col, sticky=NSEW, padx = 20)
side_B = Text(tk)
side_B.grid(row=6, column=col, sticky=NSEW, padx = 20)
side_B.insert(END,sample_sideB)
side_B.config(width = 35, height = 10)
#__________________________


#______Submit Button____________________________________#
sumbit = Button(tk,text = 'Submit')						#
sumbit.grid(row=7, column = 5, sticky = E, padx = 20)	#
sumbit.bind("<Button-1>", submitButton)					#
#_______________________________________________________#

#tk.grid_rowconfigure(0, weight=1)
#tk.grid_rowconfigure(7, weight=1)
tk.grid_columnconfigure(0, weight=1)
tk.grid_columnconfigure(5, weight=1)

tk.mainloop()

#createMenu()