import board
import digitalio
import busio
import time
import init_screen
import struct

write = init_screen.write
_CASET = init_screen._CASET
_PASET = init_screen._PASET
_RAMWR = init_screen._RAMWR
spi = init_screen.spi

#pack RGB
def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


#two 16 bit ints, big endian
def four_bytes(num1, num2):
	return struct.pack(">HH", num1, num2)
#one 16 bit int, big endian
def two_bytes(num1):
	return struct.pack(">H", num1)

#This function creates a buffer the same size as a rectangle
def make_rect(x,y, r, g,b):
	c_encoded = color565(r, g, b)
	c_ordered = two_bytes(c_encoded)
	print([c_encoded])
	print(bytearray(c_ordered))
	b_array = b""
	print(c_ordered)
	for i in range(x*y):
		b_array+=c_ordered
	return b_array
	


#writes a buffe the length of the screen to fill
def solid_fill(buffer):
	write(_CASET, four_bytes(0,319))
	write(_PASET, four_bytes(0,239))
	write(_RAMWR)
	init_screen.dc_pin.value = 1
	init_screen.cs_pin.value = 0
	for i in range(240):
		spi.write(buffer)
	init_screen.cs_pin.value = 1
#very slow, shows the importance of sending as much data in one tx as possible
def solid_fill_bad():
	write(_CASET, four_bytes(0,319))
	write(_PASET, four_bytes(0,239))
	write(_RAMWR)
	init_screen.dc_pin.value = 1
	init_screen.cs_pin.value = 0
	for i in range(320*240):
		spi.write(b"\x00\x00")
	init_screen.cs_pin.value = 1	

#writes a buffer at screen address - determined by _MADCTL
#zero indexing
def write_at(start_x, start_y, end_x, end_y, buffer):
	write(_CASET, four_bytes(start_x, end_x-1))
	write(_PASET, four_bytes(start_y, end_y-1))
	write(_RAMWR)
	init_screen.dc_pin.value = 1
	init_screen.cs_pin.value = 0
	spi.write(buffer)
	init_screen.cs_pin.value = 1

#columns = X
# rows = y
#screen coordinate linearly is y*x+x
if __name__ == "__main__":
	init_screen.init_screen()
	solid_fill_bad()
	LINE = make_rect(1,320,0,200,200)
	
	solid_fill(LINE)	
	rect = make_rect(30,30,2,20,0)

	write_at(10,10,39,39,rect)
