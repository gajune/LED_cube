import pyControllerMain
import pygame
import sys

class SpaceGame(pyControllerMain.PyControllerMain):
	def __init__(self, *args, **kwargs):
		super(SpaceGame, self).__init__(*args, **kwargs)
		self.movableObjects = []
		self.fps = 40

	def setup(self):
		print ("setting up")
		pygame.init()
		pygame.display.set_mode((400, 300))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Space Shooter 9001')
		self.player = PlayerObject()
		self.player.setSize(2)
		self.movableObjects.append(self.player)
		super(SpaceGame, self).setup()

	def gameLoop(self):
		self.clock.tick(self.fps)
		while True:
			self.update()
			self.draw()
			self.clock.tick(self.fps)


	def initJoystick(self):
		joystickNr = 0
		pygame.init()
		pygame.joystick.init()
		self.joystick = pygame.joystick.Joystick(joystickNr)
		self.joystick.init()

	def update(self):
		#print ("updating")
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_w]):
			self.player.move(0, 1, 0)
		elif (keys[pygame.K_s]):
			self.player.move(0, -1, 0)

		if (keys[pygame.K_d]):
			self.player.move(1, 0, 0)
		elif (keys[pygame.K_a]):
			self.player.move(-1, 0, 0)

		if (keys[pygame.K_UP]):
			self.player.move(0, 0, 1)
		elif (keys[pygame.K_DOWN]):
			self.player.move(0, 0, -1)

			if event.type == pygame.QUIT:
				print ("QUITTING")
				pygame.quit()
				sys.exit()
		#map(lambda o:o.update(), self.movableObjects)
		for movObj in self.movableObjects:
			movObj.update()

	def draw(self):
		self.clearAllPixel()

		for obj in self.movableObjects:
			pos, sizeX, sizeY, sizeZ = obj.draw()
			posx, posy, posz = pos.getPosition()
			for x in range(sizeX):
				for y in range(sizeY):
					for z in range(sizeZ):
						self.setPixelOn(posx + x, posy + y, posz + z)

		super(SpaceGame, self).draw()

class Position(object):
	def __init__(self, *args, **kwargs):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

	def setPosition(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def getPosition(self):
		return self.x, self.y, self.z


class MovableObject(object):
	def __init__(self, *args, **kwargs):
		self.position = Position()
		self.speedX = 0.0
		self.speedY = 0.0
		self.speedZ = 0.0
		#might have an 3d array to describe how it looks instead?
		self.sizeX = 0
		self.sizeY = 0
		self.sizeZ = 0

	def setSize(self, size):
		self.sizeX = size
		self.sizeY = size
		self.sizeZ = size

	def update(self):
		x, y, z = self.position.getPosition()
		self.position.setPosition(x + self.speedX, y + self.speedY, z + self.speedZ)

	def draw(self):
		return self.position, self.sizeX, self.sizeY, self.sizeZ
		#return a matching representation, to OR in with main array

class PlayerObject(MovableObject):
	def __init__(self, *args, **kwargs):
		self.PLAYER_UPDATE_SPEED = 0.1
		super(PlayerObject, self).__init__(*args, **kwargs)

	def update(self):
		#Check for key presses, and set speeds accordingly

		#TODO: fix, one keypress = one move, or not?

		super(PlayerObject, self).update()

	def move(self, x, y, z):
		posx, posy, posz = self.position.getPosition()
		posx += x
		posy += y
		posz += z
		#keep player in bounds of cube
		if 0 <= posx <= 8 -self.sizeX and 0 <= posy <= 8 -self.sizeY and 0 <= posz <= 8 -self.sizeZ:
			self.position.setPosition(posx, posy, posz)

if __name__ == '__main__':
	spaceGame = SpaceGame()
	spaceGame.setup()
	spaceGame.gameLoop()
