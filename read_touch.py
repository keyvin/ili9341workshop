import board
import digitalio
import busio
import struct
import time
touch_cs_pin = digitalio.DigitalInOut(board.D6)
ili9341_cs_pin = digitalio.DigitalInOut(board.D5)
interrupt_pin = digitalio.DigitalInOut(board.D17)
touch_cs_pin.direction = digitalio.Direction.OUTPUT
interrupt_pin.direction = digitalio.Direction.INPUT
ili9341_cs_pin.direction = digitalio.Direction.OUTPUT
touch_cs_pin.value = 1
ili9341_cs_pin.value = 1

#touch upper left, then bottom right to get these values
upper_left =  (240,232)
bottom_right = (136, 136)

#These values are 0-n-1 when calculated
touch_rect_columns = 10
touch_rect_rows = 8

#values used for touch values to screen mapping
x_rect_size = (upper_left[0]-bottom_right[0])/touch_rect_columns
y_rect_size = (upper_left[1]-bottom_right[1])/touch_rect_rows

#functions to put touches in specific rows and columns
def calc_row(y):
	return int((upper_left[0]-y)/y_rect_size)
def calc_column(x):
	return int((upper_left[1]-x)/x_rect_size)
spi = board.SPI()

#eight bit values read, see datasheet for bit mappings
_READ_Z = 0xcB
_READ_X = 0x9B
_READ_Y = 0xdB
_READ_Y_STOP = 0xd0

#ensure  display driver is not enabled

def read_touch_spi(command, buffer, bytes):
	spi.readinto(buffer, write_value=command)

#predefine a read_buffer to avoid dynamic allocation	
read_buffer = bytearray(3)

def read_touch(debug=False):
	while interrupt_pin.value == 1 and debug==True:
		pass
	touch_cs_pin.value =  0
	ili9341_cs_pin.value = 1
#take three readings and use the third.
	read_touch_spi(_READ_X, read_buffer, 3)
	xt = read_buffer[2]
	read_touch_spi(_READ_Y_STOP, read_buffer, 3)
#take three readings and use the third
	yt = read_buffer[2]
	touch_cs_pin.value = 1
	if(debug==True):
		print("Raw x,y values - (%d, %d)" % (xt, yt))
	touch_cs_pin.value = 1
	return (calc_column(xt),calc_row(yt)) 

if __name__=="__main__":
	while True:
		print("column(x), row (y) - (%d, %d)"%read_touch(debug=True)) 
		time.sleep(2)
