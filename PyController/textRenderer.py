import pyControllerMain
import sys
import serial
import threading
import time
import fontData

class TextRenderer(pyControllerMain.PyControllerMain):
	def __init__(self, *args, **kwargs):
		super(TextRenderer, self).__init__(*args, **kwargs)
		self.text = "HELLO "
		self.count = 0.0
		self.font = fontData.font
	def setup(self):
		port = "COM3"
		baud = 115200
		if len(sys.argv) == 4:
			port = sys.argv[1]
			baud = sys.argv[2]
			self.text = sys.argv[3]
		else:
			print ("USAGE: 'python pyController.py PORT BAUDRATE TEXT'")
			print ("Using default values: " + port + ", " + str(baud) + ", " + self.text)

		self.arduino = serial.Serial(port, baud, timeout=0)
		time.sleep(5)
		self.mainLoop()

	def update(self):
		self.count += 0.05

		index = int((self.count / 1.0) % len(self.text))

		charPos = (self.count * 8) % 8

		#Character positions for display
		pos = int((int(self.count) % (len(self.text) / 1)) * 1)
		posLeft = (pos - 1) % len(self.text)
		posRight = (pos + 1) % len(self.text)
		posLeftMost = (pos - 2) % len(self.text)
		posRightMost = (pos + 2) % len(self.text)

		for z in range(0, 8):
			index = (int(z) << 3) + 7

			#front side
			self.pixelData[index] = (((self.font[ord(self.text[pos])][7 - z] << 8) >> int(charPos)) | 
									((self.font[ord(self.text[posRight])][7 - z] << 16) >> int(charPos)) | 
									((self.font[ord(self.text[posLeft])][7 - z] << 0) >> int(charPos))
									) & 0xFF

			#right side
			displayRight = (((self.font[ord(self.text[posRight])][7 - z] << 8) >> int(charPos)) | 
									((self.font[ord(self.text[posRightMost])][7 - z] << 16) >> int(charPos)) | 
									((self.font[ord(self.text[pos])][7 - z] << 0) >> int(charPos))
									) & 0xFF

			#left side
			displayLeft = (((self.font[ord(self.text[posLeft])][7 - z] << 8) >> int(charPos)) | 
									((self.font[ord(self.text[pos])][7 - z] << 16) >> int(charPos)) | 
									((self.font[ord(self.text[posLeftMost])][7 - z] << 0) >> int(charPos))
									) & 0xFF

			#loop to help position correct bit data for sides
			for sideY in range(1, 8):
				index = (int(z) << 3) + (7 - int(sideY))
				self.pixelData[index] = (displayRight << (7 - sideY)) & 0x80
				self.pixelData[index] |= (displayLeft >> (7 - sideY)) & 0x01


if __name__ == '__main__':
	text = TextRenderer()
	text.setup()