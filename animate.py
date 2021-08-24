import init_screen
from write_screen import *
import time

init_screen.init_screen()
square_size = 20
screen_width = 320
screen_height = 240
speed_x = 10
speed_y = 10
backround =  color565(0,0,0)
forground = color565(0,200,200)
x = 40
y = 40

back_rect = make_rect(square_size, square_size, 0,0,0)
foreground_rect = make_rect(square_size,square_size,0,200,200)
LINE =  make_rect(1,screen_width,0,0,0)
solid_fill(LINE)

while True:
	write_at(x,y,x+square_size, y+square_size, back_rect)
	if (x+speed_x) < 0 or (x+square_size+speed_x) > screen_width:
		speed_x = speed_x*-1
	if (y+speed_y) < 0 or (y+square_size+speed_y) > screen_height:
		speed_y = speed_y*-1
	x = x + speed_x
	y= y + speed_y
	write_at(x,y,x+square_size, y+square_size, foreground_rect)
	time.sleep(.3)


