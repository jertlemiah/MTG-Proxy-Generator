#Author: Jeremiah Plauche

# createCard contains all of the logic for drawing the cards themselves. 
# When a FACE instance is called, it uses this class to handle the actual creation of the visuals

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
cw = '#CACCC8' #rgb(202,204,200)
color_wMana = '#FCFCC1' #rgb(252,252,193)

	#Blue
cu = '#127CAC' #rgb(18,124,172)
color_uMana = '#67C1F5' #rgb(103,193,245)

	#Black
cb = '#363732' #rgb(54,55,50)
color_bMana = '#848484' #rgb(132,132,132)

	#Red
cr = '#D85950' #rgb(216,89,80)
color_rMana = '#F85555' #rgb(248,85,85)
cr_pale =  '#D8857F' #rgb(216,133,12)

	#Green
cg = '#1F7751' #rgb(31, 119,81)
#cg_mana = '#26B569' #rgb(38,181,105)
color_gMana = '#90C3A1' #rgb(144,195,161)

	#Colorless
color_cMana = '#CCC2C0' #rgb(204,194,192)

#"Gold" Card
cgold = '#D5C089' #rgb(213,192,137)

#_____fonts_____
fnt_Bel_lg = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",35)
fnt_Bel_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",27)
fnt_italic = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MPLANTINIT.TTF",30)
fnt_magic = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MAGICSYMBOLS2008.TTF",45)
fnt_magic_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MAGICSYMBOLS2008.TTF",40)

fnt_mana = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016.TTF",44)
fnt_mana_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MTG2016.TTF",34)

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
manaCipher = {
	#Mono mana, color1 "O"; EX: OW
	"W":  (0, "W", color_wMana),
	"U":  (0, "U", color_uMana),
	"B":  (0, "B", color_bMana),
	"R":  (0, "R", color_rMana),
	"G":  (0, "G", color_gMana),
	"C":  (0, "C", color_cMana),

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

	fullCard.save("Full Card.png")

	fullCard.show()
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

	multicolor = False
	if 'Land' in card_type:
		for icon in card_colorID:
			i += 1
			if i >= 2:
				multicolor = True
	else:
		for icon in card_color:
			i += 1
			if i >= 2:
				multicolor = True

	#_____Create Image Canvas_____
	blank_image = Image.new('RGBA', (width, height), 'black')
	img_draw = ImageDraw.Draw(blank_image)
	if side == 'A':
		img_draw.rectangle((2,2,width-2,height-2),fill = 'white')

	#_____Colored Border_____
	pt1 = (offset-5,offset-10)
	pt2 = (width-offset+5,height-50)
	fill_mana = color_cMana

	if 'land' in card_type:
		if 'W' in card_colorID:
			fill_mana = color_wMana
		elif 'U' in card_colorID:
			fill_mana = color_uMana
		elif 'B' in card_colorID:
			fill_mana = color_bMana
		elif 'R' in card_colorID:
			fill_mana = color_rMana
		elif 'G' in card_colorID:
			fill_mana = color_gMana
	if (multicolor):
		fill_mana = cgold
	else:
		if 'W' in card_color:
			fill_mana = color_wMana
		elif 'U' in card_color:
			fill_mana = color_uMana
		elif 'B' in card_color:
			fill_mana = color_bMana
		elif 'R' in card_color:
			fill_mana = color_rMana
		elif 'G' in card_color:
			fill_mana = color_gMana
	
	round_rectangle(img_draw, pt1, pt2, radius = 50, fill= fill_mana)

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
	img_draw.text((limit_left-4, yoff-h/2), card_type, fill='black', font = fnt_Bel_sm)


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
					xoff += w_letter - 2						#
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
					w_letter += 4								#
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
					w_letter += 4								#
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

#def createProxy(board, deck1_name, card1_name, deck2_name, card2_name)
#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
#createProxy("main","Splinter Twin","Boros Reckoner","Junk","Reaper King")
#createProxy("side","Splinter Twin","Island","Junk","Aether Hub")