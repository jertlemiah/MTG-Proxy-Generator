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
from cardClass import CARD, createProxy


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



#createProxy("main","Splinter Twin","Plains","Junk","Forest")
#createProxy("main","Splinter Twin","Mountain","Junk","Island")
#createProxy("main","Splinter Twin","Swamp","Junk","Ugin, the Spirit Dragon")
#createProxy("main","Splinter Twin","Steam Vents","Junk","Zealous Persecution").show()
#createProxy("main","Splinter Twin","Reaper King","Junk","Chandra, Torch of Defiance").show()
#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge").show()
createProxy("main","Splinter Twin","Nicol Bolas, God-Pharaoh","Junk","Gideon, Ally of Zendikar").show()
#createProxy("main","Splinter Twin","Driven // Despair","Junk","Triumph of Gerard").show()

class createMenu():
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
		#Deck Name
		Label(self.master, text='Deck A:').grid(row=1, column=col, sticky=NSEW, padx = 20)
		self.name_A = Entry(self.master)
		self.name_A.grid(row=2, column=col, sticky=NSEW, padx = 20)
		self.name_A.insert(END,self.sample_nameA)
		self.name_A.config(width = 35)

		#Mainboard Content
		Label(self.master, text='Mainboard:').grid(row=3, column=col, sticky=NSEW, padx = 20)

		self.scroll_mainA = Scrollbar(master)
		self.scroll_mainA.grid(row=4, column=col+1, sticky=NSEW)

		self.main_A = Text(self.master, yscrollcommand=self.scroll_mainA.set)
		self.main_A.grid(row=4, column=col, sticky=NSEW)
		self.main_A.insert(END,self.sample_mainA)
		self.main_A.config(width = 35, height = 20)

		#Sideboard Contect
		Label(self.master, text='Sideboard:').grid(row=5, column=col, sticky=NSEW, 
			padx = 20)
		self.side_A = Text(self.master)
		self.side_A.grid(row=6, column=col, sticky=NSEW, padx = 20)
		self.side_A.insert(END,self.sample_sideA)
		self.side_A.config(width = 35, height = 10)
		#__________________________

		#__________DECK B__________#
		col = 3
		#Deck Name
		Label(self.master, text='Deck B:').grid(row=1, column=col, sticky=NSEW, padx = 20)
		self.name_B = Entry(self.master)
		self.name_B.grid(row=2, column=col, sticky=NSEW, padx = 20)
		self.name_B.insert(END,self.sample_nameB)
		self.name_B.config(width = 35)

		#Mainboard Content
		Label(self.master, text='Mainboard:').grid(row=3, column=col, sticky=NSEW)

		self.scroll_mainB = Scrollbar(self.master)
		self.scroll_mainB.grid(row=4, column=col, sticky=NSEW, padx = 20)
		self.scroll_mainB.config(width = 5)

		self.main_B = Text(self.master, yscrollcommand=self.scroll_mainB)
		self.main_B.grid(row=4, column=col, sticky=NSEW, padx = 20)
		self.main_B.insert(END,self.sample_mainB)
		self.main_B.config(width = 35, height = 20)

		#Sideboard Contect
		Label(self.master, text='Sideboard:').grid(row=5, column=col, sticky=NSEW, padx = 20)
		self.side_B = Text(self.master)
		self.side_B.grid(row=6, column=col, sticky=NSEW, padx = 20)
		self.side_B.insert(END,self.sample_sideB)
		self.side_B.config(width = 35, height = 10)
		#__________________________


		#______Submit Button____________________________________#
		self.sumbit = Button(self.master,text = 'Submit')						#
		self.sumbit.grid(row=7, column = 5, sticky = E, padx = 20)	#
		self.sumbit.bind("<Button-1>", self.submitButton)					#
		#_______________________________________________________#

		#tk.grid_rowconfigure(0, weight=1)
		#tk.grid_rowconfigure(7, weight=1)
		self.master.grid_columnconfigure(0, weight=1)
		self.master.grid_columnconfigure(5, weight=1)

		#tk.mainloop()

	def submitButton (self,event):
		#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
		deckA = self.name_A.get()
		deckB = self.name_B.get()

		mainA = self.main_A.get(1.0, END)
		mainB = self.main_B.get(1.0, END)

		sideA = self.side_A.get(1.0,END)
		sideB = self.side_B.get(1.0,END)

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

master = Tk()
menu = createMenu(master)
master.mainloop()

