from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas as canvas2

WIDTH = 750
HEIGHT = 1050 

def createCanvas():
	canvas = Image.new('RGBA', 
		(WIDTH, HEIGHT), 'black')
	drawCanvas = ImageDraw.Draw(canvas)
	drawCanvas.rectangle(
		(2,2,WIDTH-2,HEIGHT-2), 
		fill = 'white')
	return canvas

card = createCanvas()
card.show()

#fullCard.show()
#fullCard = Image.new('RGBA', (width, height*2), 'black')
#self.canvas.show()

def createPDF(proxyList):
	#createProxy("main","Splinter Twin","Tasigur, the Golden Fang","Junk","Vault Skirge")
	c = canvas2.Canvas("bestiary.pdf")
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
