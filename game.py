import pygame, sys, time
import pickle, random, copy
from pygame.locals import *

from game_modules import *
#Functions

from game_logic import *
#Model, Sprite(s)

pygame.init()

# Dependency: Model(loose)
class Camera(object):
	def __init__(self,model,window):
		self.model = model
		self.window = window
		self.coords = [0,0]
		self.finished = False
		
	def load(self,ts,colordict,imagedict):
		self.ts = ts
		self.colordict = colordict
		self.imagedict = imagedict
		for i in imagedict:
			imagedict[i] = pygame.image.load(imagedict[i])
	def show(self):
		x = self.coords[0]
		if x < 0: x = 0
		if not self.finished:
			self.window.fill(BLACK)
			while  x != self.model.size[0] and x != self.coords[0] + 1 + 800/self.ts:
				y = self.coords[1]
				if y < 0: y = 0
				while y != self.model.size[1] and y != self.coords[1] + 1 + 600/self.ts:
					pos = apply(applyFactor(self.coords,-1),[x,y])
					rect = pygame.Rect(applyFactor(pos,self.ts),(self.ts,self.ts))
					color = self.colordict[self.model.tiles[x][y]]
					pygame.draw.rect(self.window,color,rect)
					y += 1
				x += 1
			self.finished = False
		for coord in self.model.moved:
			pos = apply(applyFactor(self.coords,-1),coord)
			rect = pygame.Rect(applyFactor(pos,self.ts),(self.ts,self.ts))
			color = self.colordict[self.model.tiles[coord[0]][coord[1]]]
			pygame.draw.rect(self.window,color,rect)
		for row in self.model.grid:
			for sprite in row:
				if sprite != None:
					pos = apply(applyFactor(self.coords,-1),sprite.coords)			
					self.window.blit(self.imagedict[sprite.color],applyFactor(pos,self.ts))
					if sprite.type == "human":
						rect = pygame.Rect(applyFactor(apply(pos,sprite.goal),self.ts),(self.ts,self.ts))
						pygame.draw.rect(self.window,BLUE,rect, 1)
	def move(self,coords):
		self.coords = apply(self.coords,coords)
		self.finished = False

# Dependency: Model(loose), Camera(loose)
class FileLoader(object):
	def __init__(self,model,camera):
		self.model = model
		self.camera = camera
	def load(self, filenametile, filenamesprite):
		f = open(filenametile,"r")
		o = pickle.load(f)
		size = o[0]
		tiles = o[1]
		ts = o[2]
		colordict = o[3]		
		f = open(filenamesprite,"r")
		o = pickle.load(f)
		imagedict = o[0]
		sprites = o[1]
		
		self.model.loadTiles(size,tiles)
		self.model.loadSprites(sprites)
		
		self.camera.load(ts,colordict,imagedict)
		
# Dependency: Camera(loose)
class Controller(object):
	def __init__(self,camera):
		self.stickylist = []
		self.camera = camera
	def control(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				pass
			elif event.type == KEYDOWN:
				addlist = []
				if event.key == K_UP:
					addlist += ["up"]
				if event.key == K_DOWN:
					addlist += ["down"]
				if event.key == K_LEFT:
					addlist += ["left"]
				if event.key == K_RIGHT:
					addlist += ["right"]
				for a in addlist:
					if not a in self.stickylist:
						self.stickylist.append(a)
			elif event.type == KEYUP:
				removelist = []
				if event.key == K_UP:
					removelist += ["up"]
				if event.key == K_DOWN:
					removelist += ["down"]
				if event.key == K_LEFT:
					removelist += ["left"]
				if event.key == K_RIGHT:
					removelist += ["right"]
				for r in removelist:
					if r in self.stickylist:
						self.stickylist.remove(r)
	def applySticky(self):
		for s in self.stickylist:
			if s == "up":
				self.camera.move([0,-1])
			if s == "down":
				self.camera.move([0,1])
			if s == "left":
				self.camera.move([-1,0])
			if s == "right":
				self.camera.move([1,0])

# Dependency: FileLoader, Model, Camera, Controller
class Loop(object):
	def __init__(self):
		self.window = pygame.display.set_mode((800,600))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Game Refactor 3")
		self.model = Model()
		self.camera = Camera(self.model, self.window)
		self.fileloader = FileLoader(self.model, self.camera)
		self.controller = Controller(self.camera)
		self.fileloader.load("tiles.game","sprites.game")
		# Game-specific #
		for i in xrange(1000):
			self.model.physics(type="tree")
		random.seed()
		# End Game-specific #
		self.loop()
	def loop(self):
		halftimer = 0
		slowtimer = 0
		daytimer = 0
		timeprev = 0.0
		while True:
			#self.window.fill(BLACK)
			self.camera.show()
			
			pygame.display.update()
			self.controller.control()
			self.controller.applySticky()	
			
			self.clock.tick(30)
			self.model.moved = []
			if halftimer == 1:
				self.model.physics(type="human",taxation=1)			
			elif halftimer == 2:
				self.model.physics(type="human",taxation=2)
				halftimer = 0
			else:
				halftimer += 1
			if slowtimer == 8:
				for i in range(1):
					self.model.physics(type="tree")
				slowtimer = 0
				daytimer += 1
			else:
				slowtimer += 1
			if daytimer == 24:
				daytimer = 0
			if daytimer == 18:
				self.model.night = True
			if daytimer == 6:
				self.model.night = False
			
			timemodel = time.time()
			print " time, time model", (timemodel - timeprev)*30
			timeprev = timemodel
Loop()