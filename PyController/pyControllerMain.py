import sys
import serial
import threading
import time
import struct

#main class for interfacing with the cube
class PyControllerMain(object):
	def __init__(self):
		self.updateInterval = 1.0 / 50.0
		self.arduino = None
		self.pixelData = bytearray(64)

	def setup(self):
		port = "COM3"
		baud = 115200
		if len(sys.argv) == 3:
			port = sys.argv[1]
			baud = sys.argv[2]
		else:
			print ("USAGE: 'python pyController.py PORT BAUDRATE'")
			print ("Using default values: " + port + ", " + str(baud))
		self.arduino = serial.Serial(port, baud, timeout=0)
		time.sleep(5)
		self.mainLoop()

	def mainLoop(self): 
		threading.Timer(self.updateInterval, self.mainLoop).start()
		self.update()
		self.draw()

	#update should be overridden in subclass
	def update(self):
		print ("NOT IMPLEMENTED")

	def draw(self):
		self.arduino.write(self.pixelData)

	#x from left to right, y from front to back, z from bottom to top
	def setPixelOn(self, x, y, z):
		index = (int(z) << 3) + (7 - int(y))
		self.pixelData[index] = (1 << int(x)) | self.pixelData[index]

	def setPixelOff(self, x, y, z):
		index = (int(z) << 3) + (7 - int(y))
		self.pixelData[index] = ~(1 << int(x)) & self.pixelData[index]

	def clearAllPixel(self):
		self.pixelData = [0 for x in self.pixelData]

if __name__ == '__main__':
	controller = PyControllerMain()
	controller.setup()