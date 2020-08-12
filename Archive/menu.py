from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image  

#FlipProxy

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

#00 1      2             34 5      6             78  9     		 10
#0_________________________________________________________________
#1__Deck A:_________________Deck B:________________________________
#2__[ 	                 ]__[        	         ]_________________
#3__Mainboard (60 Cards)  __Mainboard (60 Cards)  ___Example Card__
#4__[                   ]^__[                   ]^___[          ]__
#4__[                   ]^__[                   ]^___[          ]__
#4__[                   ]^__[                   ]^___[          ]__
#4__[                   ]^__[                   ]^___[          ]__
#4__[                   ]^__[                   ]^___[          ]__
#5__Sideboard (15 Cards)  __Sideboard (15 Cards)  _________________
#6__[                   ]^__[                   ]^_________________
#6__[                   ]^__[                   ]^_________________
#6__[                   ]^__[                   ]^_________________
#7_________________________________________________________________

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
	deckA = name_A.get()
	deckB = name_B.get()

	mainA = main_A.get(1.0, END)
	mainB = main_B.get(1.0, END)

	sideA = side_A.get(1.0,END)
	sideB = side_B.get(1.0,END)

	proxylist = combineLists(deckA,mainA,sideA,deckB,mainB,sideB)

	print(proxylist)

#def createMenu():
tk = Tk()
width = 75*3
height = 105*3
canvas = Canvas(tk,width = width, height = height)
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