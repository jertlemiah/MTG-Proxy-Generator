
from graphics import *
#from tkinter import *

def main():
	width = 750
	height = 525 #1050
	offset = 25

	cw = color_rgb(202,204,200)
	cu = color_rgb(18,124,172)
	cb = color_rgb(54,55,50)
	cr = color_rgb(216,89,80)
	cg = color_rgb(31, 119,81)



	win = GraphWin("My Window",width,height)
	win.setBackground('black')

	#pt1 = Point(50,50)
	#pt2 = Point(180,475)
	#rect = Rectangle(pt1,pt2)
	#rect.setFill(cw)
	#rect.draw(win)

	#pt1 = Point(180,50)
	#pt2 = Point(310,475)
	#rect = Rectangle(pt1,pt2)
	#rect.setFill(cu)
	#rect.draw(win)

	#pt1 = Point(310,50)
	#pt2 = Point(440,475)
	#rect = Rectangle(pt1,pt2)
	#rect.setFill(cb)
	#rect.draw(win)

	#pt1 = Point(440,50)
	#pt2 = Point(570,475)
	#rect = Rectangle(pt1,pt2)
	#rect.setFill(cr)
	#rect.draw(win)

	#pt1 = Point(570,50)
	#pt2 = Point(700,475)
	#rect = Rectangle(pt1,pt2)
	#rect.setFill(cg)
	#rect.draw(win)

	#tk = Tk()

	#Colored Bottom
	pt1 = Point(offset,offset)
	pt2 = Point(width-offset,525-offset)
	rect = Rectangle(pt1,pt2)
	rect.setFill(cr)
	rect.draw(win)

	#Bottom - White Fill
	pt1 = Point(offset*2,offset*2)
	pt2 = Point(width-offset*2,525-offset*2)
	rect = Rectangle(pt1,pt2)
	rect.setFill('white')
	rect.draw(win)

	#name = Text(Point(100,100),"H")#"Flamewake Phoenix")
	#name.setFace("Beleren Bold")
	#name.setSize(36)
	#name.draw(win)

	name = Text(Point(375,80),"Flamewake Phoenix")
	name.setFace("Beleren Bold")
	name.setSize(36)
	name.draw(win)

	cardtext_s = ("Flying, haste \n"
		+"Flamewake Phoenix attacks each turn if able. \n"
		+"Ferocious -  At the beginning of combat on your turn, "
		+"if you control a creature with power 4 or greater, you may pay [R], "
		+"if you do, return Flamewake Phoenix from your graveyard to the battlefield.")

	cardtext = Text(Point(375,150),cardtext_s)
	cardtext.setFace("Beleren Bold")
	cardtext.setSize(20)
	cardtext.draw(win)

	typeline = Text(Point(375,450),"Creature - Phoenix")
	typeline.setFace("Beleren Bold")
	typeline.setSize(30)
	typeline.draw(win)

	#name = Entry(Point(375,80),23)
	#name.setFace("Beleren Bold")
	#name.setText("Flamewake Phoenix")
	#name.setSize(34)
	#name.draw(win)

	win.getMouse()
	win.close()





main()