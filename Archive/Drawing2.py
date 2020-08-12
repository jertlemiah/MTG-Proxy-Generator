from tkinter import *
#from graphics import *

#def main():
#cw = color_rgb(202,204,200)
#cu = color_rgb(18,124,172)
#cb = color_rgb(54,55,50)
#cr = color_rgb(216,89,80)
#cg = color_rgb(31, 119,81)

cw = '#CACCC8'
cu = '#127CAC'
cb = '#363732'
cr = '#D85950'
cg = '#1F7751'

tk = Tk()
width = 750
height = 525

canvas = Canvas(tk,height = 525,width = 750, bg = cb)
tk.title("Card")
canvas.pack()

canvas.create_rectangle(0,0,750,525,fill=cr)

tk.mainloop()

#tk = Tk()
#canvas = Canvas(tk,height = 525,width = 750, bg = cb)
#tk.title("Card")
#canvas.pack()

#main()