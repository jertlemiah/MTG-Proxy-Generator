from PIL import Image, ImageDraw, ImageFont
import mana.css
import textwrap


width = 750
height = 525 #1050
blank_image = Image.new('RGBA', (width, height), 'black')
img_draw = ImageDraw.Draw(blank_image)

#<i class="ms ms-u"></i>