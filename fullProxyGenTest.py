# Author: Jeremiah Plauche

# This test file is a compilation of several tests

# The outputs include:
#	Created images for all "faces" of the sample cards
#	Created image for a sample full carcd that contains two "faces"

# Also A popup menu will appear for inputing a deck
# 	Clicking build initiates the build process, which is ridiculously slow at the momemt
# 	The console output should show you the progress out of the 75 sample lines

from proxyGenPythonSaves/cardClass.py import gauntlet
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
from cardClass import CARD, DECK, createProxy


#_____Various Variables_____
width = 750
height = 525 #1050
offset = 20

limit_left = 65
limit_right = width - 110

offset_name_y = 50
offset_text_y = 110
offset_type_y = height - 95  #440


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
				print(n,"/",75)
		c.showPage()

	#c.showPage() ends the current page and goes to the next one

	#c.showPage()
	c.save()
#createPDF()

def expandList(decklist):
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

def combineLists(deckname1,list1,deckname2,list2):
	combinedList = []

	main1, side1 = expandList(list1)	
	main2, side2 = expandList(list2)

	n1 = n2 = 0
	for cards in main1:
		n1 = n1+1
	for cards in main2:
		n2 = n2+1
	for i in range(max(n1,n2)):
		if i >= n1:
			singleCard = ("main",'','',deckname2,main2[i])
		elif i >= n2:
			singleCard = ("main",deckname1,main1[i],'','')
		else:
			singleCard = ("main",deckname1,main1[i],deckname2,main2[i])
		combinedList.append(singleCard)

	n1 = n2 = 0
	for cards in side1:
		n1 = n1+1
	for cards in side2:
		n2 = n2+1
	for i in range(max(n1,n2)):
		if i >= n1:
			singleCard = ("side",'','',deckname2,side2[i])
		elif i >= n2:
			singleCard = ("side",deckname1,side1[i],'','')
		else:
			singleCard = ("side",deckname1,side1[i],deckname2,side2[i])
		combinedList.append(singleCard)

	return combinedList


#createProxy("main","Splinter Twin","Plains","Junk","Forest")
#createProxy("main","Splinter Twin","Mountain","Junk","Island")
#createProxy("main","Splinter Twin","Swamp","Junk","Ugin, the Spirit Dragon")
#createProxy("main","Splinter Twin","Steam Vents","Junk","Zealous Persecution").show()
#createProxy("main","Splinter Twin","Reaper King","Junk","Chandra, Torch of Defiance").show()
#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge").show()
#createProxy("main","Splinter Twin","Nicol Bolas, God-Pharaoh","Junk","Gideon, Ally of Zendikar").show()
#createProxy("main","Splinter Twin","Driven // Despair","Junk",).show()

class createMenu():
	#__Sample Decks___________________________________
	sample_deckNames = ('Bant Spirits','BR Hollow One')
	sample_deckLits = {
	'Bant Spirits': "//Main"
		+ "\n2 Anafenza, Kin-Tree Spirit"
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
		+ "\n3 Windswept Heath"
		+ "\n"
		+ "\n//Sideboard"
		+ "\nSB: 2 Engineered Explosives"
		+ "\nSB: 1 Kira, Great Glass-Spinner"
		+ "\nSB: 2 Negate"
		+ "\nSB: 2 Path to Exile"
		+ "\nSB: 2 Qasali Pridemage"
		+ "\nSB: 3 Rest in Peace"
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

	def __init__(self, master):
		#http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
		#tk = Tk()
		self.master = master

		menuWidth = 75*3
		menuHeight = 105*3
		canvas = Canvas(self.master,width = menuWidth, height = menuHeight)
		canvas.grid(row = 4, column = 6)
		img = ImageTk.PhotoImage(Image.open("Full Card.png"))
		canvas.create_image(0,0,anchor=NW,image = img)

		#__________DECK A__________#
		col = 1
		width = 35
		#Deck Name
		deckName = self.sample_deckNames[0]
		deckList = self.sample_deckLits[deckName]

		Label(self.master, text='Deck Name:').grid(row=1, column=col, sticky=NSEW, padx = 20)
		self.decknameA = Entry(self.master)
		self.decknameA.grid(row=2, column=col, sticky=NSEW, padx = 20)
		self.decknameA.insert(END,deckName)
		self.decknameA.config(width = width)

		#Decklist
		Label(self.master, text='Decklist:').grid(row=3, column=col, sticky=NSEW, padx = 20)
		self.decklistA = Text(self.master)
		self.decklistA.grid(row=4, column=col, sticky=NSEW, padx = 20)
		self.decklistA.insert(END,deckList)
		self.decklistA.config(width = width, height = 20)
		#__________________________

		#__________DECK B__________#
		col = 3
		#Deck Name
		deckName = self.sample_deckNames[1]
		deckList = self.sample_deckLits[deckName]

		Label(self.master, text='Deck Name:').grid(row=1, column=col, sticky=NSEW, padx = 20)
		self.decknameB = Entry(self.master)
		self.decknameB.grid(row=2, column=col, sticky=NSEW, padx = 20)
		self.decknameB.insert(END,deckName)
		self.decknameB.config(width = width)

		#Decklist
		Label(self.master, text='Decklist:').grid(row=3, column=col, sticky=NSEW)
		self.decklistB = Text(self.master)
		self.decklistB.grid(row=4, column=col, sticky=NSEW, padx = 20)
		self.decklistB.insert(END,deckList)
		self.decklistB.config(width = width, height = 20)
		#__________________________

		#______Submit Button____________________________________#
		self.sumbit = Button(self.master,text = 'Submit')						#
		self.sumbit.grid(row=2, column = 5, sticky = E, padx = 20)	#
		self.sumbit.bind("<Button-1>", self.submitButton)					#
		#_______________________________________________________#

		#tk.grid_rowconfigure(0, weight=1)
		#tk.grid_rowconfigure(7, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		self.master.grid_columnconfigure(6, weight=1)

		#tk.mainloop()

	def submitButton (self,event):
		deckNameA = self.decknameA.get()
		deckNameB = self.decknameB.get()

		listA = self.decklistA.get(1.0, END)
		listB = self.decklistB.get(1.0, END)

		deck = DECK(deckNameA = deckNameA, 
			deckListA = listA,
			deckNameB = deckNameB,
			deckListB = listB)

		deck.printList()

		#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
		'''
		proxyList = combineLists(deckname1 = deckNameA,
			list1 = listA,
			deckname2 = deckNameB,
			list2 = listB)
			#deckA,mainA,sideA,deckB,mainB,sideB)
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

		#createPDF(proxyList)
		i = 1
		for things in proxyList:
			validate(things)

			things[2] #Deck A card name

			self.card = cardSearch(cardName) #card is a dictionary
			self.layout = self.card['layout']

			if self.layout == 'transform':
			side1 = self.card['card_faces'][0]['name']
			side2 = self.card['card_faces'][1]['name']
			self.appendix.add((side1, side2))


			try:
				card = cardSearch(cardName)
			except:

			print(i,things)
			i = i+1
		#print(proxyList)
		'''	
		print("DONE!")
		#createPDF(proxyListImg)	
		#print(proxylist)

#gauntletTest = cardClass

gauntlet()	# creates images for every test case

master = Tk()
menu = createMenu(master)
master.mainloop()

