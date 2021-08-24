import board
import digitalio
import busio
import time


cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
cs_pin.direction = digitalio.Direction.OUTPUT
dc_pin.direction = digitalio.Direction.OUTPUT
reset_pin.direction = digitalio.Direction.OUTPUT
reset_pin.Value = 1
cs_pin.Value = 1
reset_pin.Value = 1

BAUDRATE = 30000000

_RDDSDR = 0x0f # Read Display Self-Diagnostic Result
_SLPOUT = 0x11 # Sleep Out
_GAMSET = 0x26 # Gamma Set
_DISPOFF = 0x28 # Display Off
_DISPON = 0x29 # Display On
_CASET = 0x2a # Column Address Set
_PASET = 0x2b # Page Address Set
_RAMWR = 0x2c # Memory Write
_RAMRD = 0x2e # Memory Read
_MADCTL = 0x36 # Memory Access Control
_VSCRSADD = 0x37 # Vertical Scrolling Start Address
_PIXSET = 0x3a # Pixel Format Set
_PWCTRLA = 0xcb # Power Control A
_PWCRTLB = 0xcf # Power Control B
_DTCTRLA = 0xe8 # Driver Timing Control A
_DTCTRLB = 0xea # Driver Timing Control B
_PWRONCTRL = 0xed # Power on Sequence Control
_PRCTRL = 0xf7 # Pump Ratio Control
_PWCTRL1 = 0xc0 # Power Control 1
_PWCTRL2 = 0xc1 # Power Control 2
_VMCTRL1 = 0xc5 # VCOM Control 1
_VMCTRL2 = 0xc7 # VCOM Control 2
_FRMCTR1 = 0xb1 # Frame Rate Control 1
_DISCTRL = 0xb6 # Display Function Control
_ENA3G = 0xf2 # Enable 3G
_PGAMCTRL = 0xe0 # Positive Gamma Control
_NGAMCTRL = 0xe1 # Negative Gamma Control

ROTATION_0 = 0x48 #default is portrait
ROTATION_90 = 0x28 #we want landscape
#spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi = board.SPI()

while not spi.try_lock():
	pass
spi.configure(baudrate=BAUDRATE, phase=0, polarity=0)
spi.unlock()
reset_pin.value = 1
def write(command, data=""):
	dc_pin.value = 0
	cs_pin.value = 0
	spi.write(bytearray([command]))
	if not data == None:
		dc_pin.value = 1	
		spi.write(data)
	cs_pin.value = 1


def init_screen():
	for command, data in (
		(_RDDSDR, b"\x03\x80\x02"),
        	(_PWCRTLB, b"\x00\xc1\x30"),
        	(_PWRONCTRL, b"\x64\x03\x12\x81"),
        	(_DTCTRLA, b"\x85\x00\x78"),
        	(_PWCTRLA, b"\x39\x2c\x00\x34\x02"),
        	(_PRCTRL, b"\x20"),
        	(_DTCTRLB, b"\x00\x00"),
        	(_PWCTRL1, b"\x23"),
        	(_PWCTRL2, b"\x10"),
        	(_VMCTRL1, b"\x3e\x28"),
        	(_VMCTRL2, b"\x86")):
		write(command, data)
#our orientation
	write(_MADCTL, b"\x28")
	for command, data in (
		(_PIXSET, b"\x55"),
        	(_FRMCTR1, b"\x00\x18"),
        	(_DISCTRL, b"\x08\x82\x27"),
        	(_ENA3G, b"\x00"),
        	(_GAMSET, b"\x01"),
        	(_PGAMCTRL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
        	(_NGAMCTRL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
		write(command, data)
	write(_SLPOUT)
	time.sleep(.120)
	write(_DISPON)

if __name__=="__main__":
	init_screen()
