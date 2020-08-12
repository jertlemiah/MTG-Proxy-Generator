from PIL import Image, ImageDraw, ImageFont
import textwrap
from math import atan2

def my_isSplit(char):
    splitMana = {'e','H','V','J','E','M','D','d','K','F'}
    for c in splitMana:
        if char in splitMana: return True
    return False
 
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

def draw_namebox(canvas, point1, point2, fill):
    """Draw a rounded rectangle"""
    x1, y1 = point1
    x2, y2 = point2

    radius = (((x2-x1)/(2))**2+((y2-y1)/(2))**2)**0.5+10
    theta = atan2(((y2+y1)/2),((x2+x1)/2))
    theta = theta*(180/3.14)/2
    canvas.ellipse(((x2+x1)/2-radius, (y2+y1)/2-50, ((x2+x1)/2+radius)/4, (y2+y1)/2+50),
     fill=fill)
    #canvas.pieslice(((x2+x1)/2-radius, (y2+y1)/2-radius*2, ((x2+x1)/2+radius)/4, (y2+y1)/2+radius*2),
    # 180-theta, 180+theta, fill=fill)
    canvas.rectangle((point1, point2), fill = fill)


#_____fonts_____
fnt_Bel_lg = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",35)
fnt_Bel_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\BELEREN-BOLD_P1.01.TTF",29)
fnt_magic = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MAGICSYMBOLS2008.TTF",45)
fnt_magic_sm = ImageFont.truetype("C:\\WINDOWS\\FONTS\\MAGICSYMBOLS2008.TTF",40)

#_____Colors_____
	#White
cw = '#CACCC8' #rgb(202,204,200)
cw_mana = '#FCFCC1' #rgb(252,252,193)

	#Blue
cu = '#127CAC' #rgb(18,124,172)
cu_mana = '#67C1F5' #rgb(103,193,245)

	#Black
cb = '#363732' #rgb(54,55,50)
cb_mana = '#848484' #rgb(132,132,132)

	#Red
cr = '#D85950' #rgb(216,89,80)
cr_mana = '#F85555' #rgb(248,85,85)
cr_pale =  '#D8857F' #rgb(216,133,12)

	#Green
cg = '#1F7751' #rgb(31, 119,81)
#cg_mana = '#26B569' #rgb(38,181,105)
cg_mana = '#90C3A1' #rgb(144,195,161)

	#Colorless
cc_mana = '#CCC2C0' #rgb(204,194,192)

#w/u is e
#u/b is H
#b/r is V
#r/g is J
#g/w is E
#w/b is M
#b/G is D
#g/u is d
#u/r is K
#r/w is F

#_____Various Variables_____
width = 750
height = 525 #1050
offset = 20

limit_left = 65
limit_right = width - 105

offset_name_y = 50
offset_text_y = 115
offset_type_y = height - 95  #440

#_____Card Info_____
#card_name = "Flamewake Phoenix"
card_name = "Kira, Great Glass-Spinner"
#card_mana = "1rr"
card_mana = "1geFH"
#card_type = "Creature - Phoenix"
card_type = "Legendary Creature — Human Warrior"
#card_type = "Legendary Creature — Elder Dragon"
#card_text = ("Flying, haste "
#		+"\nFlamewake Phoenix attacks each turn if able. "
#		+"\nFerocious - At the beginning of combat on your turn, "
#		+"if you control a creature with power 4 or greater, you may pay [r]. "
#		+"If you do, return Flamewake Phoenix from your graveyard to the battlefield.")
card_text = ("Escalate — Discard a card. "
+ "(Pay this cost for each mode chosen beyond the first.) " 
+ "\nChoose one or more — "
+ "\n• [w] [u] [b] [r] [g] [X1294] [E] yo hoho "
#+ "\n• Target opponent reveals their hand. You choose an instant "
#+ "or sorcery card from it. That player discards that card. "
#+ "\n• Target creature gets -2/-2 until end of turn. "
+ "\n• if you control a creature with power 4 or greater, you may pay [r] . If you do "
+ "\n• Target opponent loses 2 life and you gain 2 life.")
card_pt = "20/20"



def main():
	#_____Create Image Canvas_____
	blank_image = Image.new('RGBA', (width, height), 'black')
	img_draw = ImageDraw.Draw(blank_image)

	#_____Colored Border_____
	pt1 = (offset-5,offset-10)
	#pt2 = (width-offset,height-offset)
	pt2 = (width-offset+5,height-50)
	round_rectangle(img_draw, pt1, pt2, radius = 50, fill= cg_mana)

	#img_draw.rectangle((pt1,pt2), fill = cr_mana)

	#_____White Fill_____
	#pt1 = (offset*2,offset*2)
	#pt2 = (width-offset*2,525-offset*4)
	#img_draw.rectangle((pt1,pt2), fill = 'white')

	#_____Vertical Pieces_____
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
	img_draw.text((limit_left, yoff-h/2), card_type, fill='black', font = fnt_Bel_sm)

	#_____Power/Toughness_____
	pt1 = (width-150,height-100)
	pt2 = (width-offset*2,height-50)

	inc = 8
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc,pt2[1]+inc), radius = 20+inc/2, fill= 'black')

	inc = 0
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-1), 
		(pt2[0]+inc,pt2[1]+1), radius = 15, fill= 'white')

	pt1 = (width-150,height-100)
	pt2 = (width-offset*2,height-55)

	w, h = img_draw.textsize(card_pt,font = fnt_Bel_lg)
	yoff = pt1[1]+(pt2[1]-pt1[1])/2
	xoff = pt1[0]+(pt2[0]-pt1[0])/2
	img_draw.multiline_text((xoff-w/2+2,yoff-h/2), card_pt, fill='black', font = fnt_Bel_lg)

	#_____Card Name_____
	pt1 = (offset*2,offset*2+5)
	pt2 = (width-offset*2,100-5)

	inc = 8
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc,pt2[1]+inc), radius = 20, fill= 'black')
	#draw_namebox(img_draw, pt1, pt2, fill= 'blue')

	#inc = 10
	#round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
	#	(pt2[0]+inc,pt2[1]+inc), radius = 20+inc/2, fill= cr_mana)

	#inc = 2
	#round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
	#	(pt2[0]+inc,pt2[1]+inc), radius = 20+inc/2, fill= 'black')

	inc = 0
	round_rectangle(img_draw, (pt1[0]-inc,pt1[1]-inc), 
		(pt2[0]+inc,pt2[1]+inc), radius = 10, fill= 'white')

	trash, h = img_draw.textsize(card_name, font = fnt_magic)
	yoff = pt1[1]+(pt2[1]-pt1[1])/2	

	img_draw.text((limit_left, yoff-h/2+2), card_name, fill='black', font = fnt_Bel_lg)


	#_____Mana Cost_____
	fill = { 'w': cw_mana, 'u': cu_mana, 'b': cb_mana, 'r': cr_mana, 'g': cg_mana, 
		'X': cc_mana, '0': cc_mana, '1': cc_mana, '2': cc_mana, '3': cc_mana, '4': cc_mana,
		'5': cc_mana, '6': cc_mana, '7': cc_mana, '8': cc_mana, '9': cc_mana, '3': cc_mana,
		'e': cw_mana, 'H': cu_mana, 'V': cb_mana, 'J': cr_mana, 'E': cg_mana,
		'M': cw_mana, 'D': cb_mana, 'd': cg_mana, 'K': cu_mana, 'F': cr_mana}
	fill2 = {'e': cu_mana, 'H': cb_mana, 'V': cr_mana, 'J': cg_mana, 'E': cw_mana,
		'M': cb_mana, 'D': cg_mana, 'd': cu_mana, 'K': cr_mana, 'F': cw_mana}

	w, h = img_draw.textsize(card_mana, font = fnt_magic)
	yoff = pt1[1]+(pt2[1]-pt1[1])/2	
	i=0
	xoff = 55
	for char in card_mana:	
		
		x = limit_right - w + xoff
		y = yoff-h/2-4

		if(my_isSplit(char)):
			w_letter, trash = img_draw.textsize('O', font = fnt_magic)

			img_draw.text((x-2,y+4), "O", fill='black', font = fnt_magic)			#black outline
			img_draw.text((x,y), "O", fill=fill[card_mana[i]], font = fnt_magic)	#color fill
			img_draw.text((x,y), "/", fill=fill2[card_mana[i]], font = fnt_magic)	#color fill	
		else:
			w_letter, trash = img_draw.textsize('o', font = fnt_magic)

			img_draw.text((x-2,y+4), "o", fill='black', font = fnt_magic)			#black outline
			img_draw.text((x,y), "o", fill=fill[card_mana[i]], font = fnt_magic)	#color fill

		img_draw.text((x,y), card_mana[i], fill='black', font = fnt_magic)			#mana text
		xoff += w_letter
		i += 1

	#_____Card Text_____
	trash, h = img_draw.textsize("This is an example sentence for height reasons", font=fnt_Bel_sm) #comes out to 37
	h -= 5			#lowers h to 32 for better text
	yoff = 0		#how we place the cursor
	xoff = 0		#how we place the cursor
	bullets = False
	itallics = False

	words = card_text.split(' ') #creates a list of words from the text

	for word in words:
		#print(word[0])
		symbol = False
		if (word[0]=='\n'):
			#yoff += h+10
			yoff += h + 10
			xoff = 0
			trash, word = word.split('\n')
			bullets = False
			if (word[0]=='•'):
				bullets = True

		w, trash = img_draw.textsize(word + ' ', font=fnt_Bel_sm)

		if (word[0]=='['):
			symbol = True
			stop = word.index(']')
			remains = word[stop+1:]
			word = word[1:stop]

		if (word[0] == '(' ):
			itallics = True

		if (xoff+w >= limit_right):
			yoff += h
			xoff = 0
			if (bullets):
				xoff = 20
				print('test')
		if(symbol):

			i = 0
			for char in word:	
				x = limit_left + xoff -2 #+ w_letter*i -2 
				y = offset_text_y+yoff - 5

				if(my_isSplit(char)):
					w_letter, trash = img_draw.textsize('O', font=fnt_magic_sm)

					img_draw.text((x-1,y+2), "O", fill='black', font = fnt_magic_sm)		#black outline
					img_draw.text((x,y), "O", fill=fill[word[i]], font = fnt_magic_sm)		#color fill
					img_draw.text((x,y), "/", fill=fill2[word[i]], font = fnt_magic_sm)	#color fill	
				else:
					w_letter, trash = img_draw.textsize('o', font=fnt_magic_sm)
					
					img_draw.text((x-1,y+2), "o", fill='black', font = fnt_magic_sm)	#black outline
					img_draw.text((x,y), "o", fill=fill[word[i]], font = fnt_magic_sm)	#color fill

				img_draw.text((x,y), word[i], fill='black', font = fnt_magic_sm)		#mana text
				xoff += w_letter
				i += 1
	#	if(symbol):
	#		i = 0
	#		w, trash = img_draw.textsize('o', font=fnt_magic_sm)
	#		for char in word:	
	#			#xoff += w
	#			x = limit_left-2 + xoff + w*i
	#			y = offset_text_y+yoff-5
	#
	#			img_draw.text((x-1,y+2), "o", fill='black', font = fnt_magic_sm)		#black outline
	#			img_draw.text((x,y), "o", fill=fill[word[i]], font = fnt_magic_sm)		#color fill
	#			img_draw.text((x,y), word[i], fill='black', font = fnt_magic_sm)		#mana text
	#			#xoff += w-10
	#			i += 1
	#		xoff += w*(i-1)
		else:
			img_draw.text((limit_left+xoff, offset_text_y+yoff), word + ' ', font=fnt_Bel_sm, fill='Black')
			xoff += w-1

		if (word[-1] == ')' ):
			itallics = False


	#_____Deck Name_____
	deck_name = "Bant Spirits"
	img_draw.text((limit_left,height - offset*2 ), 'Side A: ' + deck_name, fill='white', font = fnt_Bel_sm)


	blank_image.save('drawn_image.png')

	blank_image.show()

main()

#textwrapobj = textwrap.TextWrapper(width=45, replace_whitespace = False)
#wrapped_lines = textwrapobj.fill(card_text)
#img_draw.text((offset_left, offset_text_y), wrapped_lines, font=fnt_Bel_sm, fill='Black')

#for char in card_text:
#	if (char == '\n'):
#		yoff += h+10
#		xoff = 0
#	elif (xoff >= xlimit):
#		yoff += h
#		xoff = 0
#	w, trash = img_draw.textsize(char, font=fnt_Bel_sm)
#	img_draw.text((offset_left+xoff, offset_text_y+yoff), char, font=fnt_Bel_sm, fill='Black')
#	xoff += w-1

#wrapped_lines = textwrapobj.wrap(card_text)	#Create a list of lines from the string?
#i = 0
#yoffset = 0
#newlines = ''
#w, h = img_draw.textsize("This is an example sentence for height reasons", font=fnt_Bel_sm)
#for line in wrapped_lines:
#	#for char in line:
#		#if char == '\n':
#			#yoffset += 1
#			#newlines += '\n'
#	img_draw.text((offset_left, offset_text_y+yoffset), newlines + line, font=fnt_Bel_sm, fill='Black')
#	yoffset += h
#	newlines += '\n'
#	#'\n'*i
#	#i += 1

#wrapped_lines = textwrapobj.fill(card_text)

#for line in wrapped_lines:
#	print (line)
#print (wrapped_lines)
#img_draw.multiline_text((offset_left, offset_text_y), wrapped_lines, font=fnt_Bel_sm, fill='Black')