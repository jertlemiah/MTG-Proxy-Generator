#from reportlab.platypus import Image
from reportlab.pdfgen import canvas as canvas2
from reportlab.lib.units import inch
from PIL import Image, ImageDraw, ImageFont

def createPDF():
	c = canvas2.Canvas("Proxies.pdf")
	c.setPageSize((8.5*inch,11*inch))

	card_x = 2.5
	card_y = 3.5

	margin_x = 0.5
	margin_y = 0.25

	#(x,y) is bottom left corner
#	for i in range(0,3):
#		for j  in range(0,3):
#			x = margin_x + 0 + card_x*i
#			y = margin_y + 0 + card_y*j
#			print (i*3+j)
#			c.drawImage("Full Card.png", x*inch,y*inch, 
#				(card_x)*inch, (card_y)*inch)
	#for x in rand(0,100):
	#	proxyListImg.append("Full Card.png")
	#cardImage = Image.new('RGBA', (100, 100), 'black')

	for k in range(0,3):
		for i in range(0,3):
			for j  in range(0,3):
				x = margin_x + 0 + card_x*i
				y = margin_y + 0 + card_y*j
				
				#cardImage = proxyListImg(j+i*3+k*9)
				cardImage = "Full Card.png"
				c.drawInlineImage(cardImage, x*inch,y*inch, 
					(card_x)*inch, (card_y)*inch)
		c.showPage()

	c.showPage()
	c.save()
createPDF()