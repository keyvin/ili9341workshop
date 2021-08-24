import init_screen
import read_touch
from write_screen import *
import time

init_screen.init_screen()
square_size = 20
screen_width = 320
screen_height = 210
speed_x = 10
speed_y = 10
backround =  color565(0,0,0)
forground = color565(0,200,200)
x = 40
y = 40
max_speed = 20
#remember - make_rect(x_size, y_size, r, g, b)

back_rect = make_rect(square_size, square_size, 0,0,0)
foreground_rect = make_rect(square_size,square_size,0,200,200)
slow_rect = make_rect(100, 30, 200,0,0)
go_rect = make_rect(100,30,0,200,0)

LINE =  make_rect(1,screen_width,0,0,0)
STRIP = make_rect(1,screen_width,200,200,200)
solid_fill(LINE)
#remember write_at(sx,sy,ex,ey, buffer)
write_at(0, screen_height,screen_width,screen_height+1, STRIP)
write_at(30, screen_height+5, 130, screen_height+35, slow_rect)
write_at(200, screen_height+5, 300, screen_height+35, go_rect)  

times_looped = 0
last_touch = 0
read_touch.read_touch(True)

def slow_rect():
	new_speed = speed_x/abs(speed_x) * (abs(speed_x) -4) 
	new_speed = int(new_speed)
	if speed_x < 0 and new_speed > 0:
		new_speed = 0
	if speed_x > 0 and new_speed <0:
		new_speed = 0
	return (new_speed, new_speed)
def speed_rect():
	if speed_x == 0:
		return(2, 2)
	new_speed = speed_x/abs(speed_x) * (abs(speed_x) + 4)
	new_speed = int(new_speed)
	if speed_x > 0 and new_speed > max_speed:
		new_speed = max_speed
	if speed_x < 0 and new_speed < (-max_speed):
		new_speed = -max_speed	
	return (new_speed, new_speed)

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
	times_looped = times_looped+1
	if times_looped <0: 
		times_looped =0
		last_touch = 0
	#interrupt pin is low when screen is being touched
	if read_touch.interrupt_pin.value == False and times_looped-last_touch > 4:
		last_touch = times_looped
		#x is column, y is row
		col,row = read_touch.read_touch()
		print("row, col: %d, %d" %(row, col))
		if (row >= 7):
			if col >=0 and col <=3:
				speed_x, speed_y = slow_rect()
				print(speed_x)
			if col >=5 and col <=7:
				speed_y, speed_x = speed_rect()
				print(speed_x)


