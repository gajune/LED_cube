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
		time.sleep(3.5)

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
		if self.checkInterval(x, y, z):
			index = (int(z) << 3) + (7 - int(y))
			self.pixelData[index] = (1 << int(x)) | self.pixelData[index]

	def setPixelOff(self, x, y, z):
		if self.checkInterval(x, y, z):
			index = (int(z) << 3) + (7 - int(y))
			self.pixelData[index] = ~(1 << int(x)) & self.pixelData[index]

	def clearAllPixel(self):
		self.pixelData = [0 for x in self.pixelData]

	def drawLine(self, fromX, fromY, fromZ, toX, toY, toZ):
		if self.checkInterval(fromX, fromY, fromZ) and self.checkInterval(toX, toY, toZ):
			for x in range(fromX, toX + 1):
				for y in range(fromY, toY + 1):
					for z in range(fromZ, toZ + 1):
						self.setPixelOn(x, y, z)

	def checkInterval(self, x, y, z):
		return (0 <= x <= 8 and 0 <= y <= 8 and 0 <= z <= 8)

if __name__ == '__main__':
	controller = PyControllerMain()
	controller.setup()
	controller.mainLoop()
