import pyControllerMain

# A small test program that shows a sin wave on the cube
class CubeAnimation(pyControllerMain.PyControllerMain):
	def __init__(self, *args, **kwargs):
		super(CubeAnimation, self).__init__(*args, **kwargs)
		self.count = 0

	def update(self):
		self.count += 0.3 #speed adjustment
		c = int(self.count % 8)

		size = (7 - c) if (c >= 4) else c

		self.clearAllPixel()

		self.drawLine(3 - size, 3 - size, 3 - size, 4 + size, 3 - size, 3 - size)
		self.drawLine(3 - size, 3 - size, 4 + size, 4 + size, 3 - size, 4 + size)
		self.drawLine(3 - size, 4 + size, 3 - size, 4 + size, 4 + size, 3 - size)
		self.drawLine(3 - size, 4 + size, 4 + size, 4 + size, 4 + size, 4 + size)

		self.drawLine(3 - size, 3 - size, 3 - size, 3 - size, 4 + size, 3 - size)
		self.drawLine(3 - size, 3 - size, 4 + size, 3 - size, 4 + size, 4 + size)
		self.drawLine(4 + size, 3 - size, 4 + size, 4 + size, 4 + size, 4 + size)
		self.drawLine(4 + size, 3 - size, 3 - size, 4 + size, 4 + size, 3 - size)

		self.drawLine(3 - size, 3 - size, 3 - size, 3 - size, 3 - size, 4 + size)
		self.drawLine(3 - size, 4 + size, 3 - size, 3 - size, 4 + size, 4 + size)
		self.drawLine(4 + size, 3 - size, 3 - size, 4 + size, 3 - size, 4 + size)
		self.drawLine(4 + size, 4 + size, 3 - size, 4 + size, 4 + size, 4 + size)


if __name__ == '__main__':
	cube = CubeAnimation()
	cube.setup()
	controller.mainLoop()
