import pyControllerMain
import math

# A small test program that shows a sin wave on the cube
class SinWave(pyControllerMain.PyControllerMain):
	def __init__(self, *args, **kwargs):
		super(SinWave, self).__init__(*args, **kwargs)
		self.count = 0

	def update(self):
		self.count += 8 #speed adjustment
		self.clearAllPixel()
		for layer in range(0, 8):
			for y in range(0, 8):
				sinVal = math.sin(math.radians(y * 30 + self.count)) * 4
				for x in range(0, 8):
					self.setPixelOn(y,x,3.5 + sinVal)

if __name__ == '__main__':
	sinWave = SinWave()
	sinWave.setup()
	sinWave.mainLoop()
