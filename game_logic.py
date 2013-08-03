import random, copy
from game_modules import *

# Component-ize this UGLY sprite codes
# Actually, no, just make it BEAUTIFUL!
class Sprite(object):
	def __init__(self,model,coords,env):
		self.model = model
		self.type = "none"
		self.coords = coords
		self.color = env["color"]
		self.isRemove = False
	def physics(self):
		pass
		
class SpriteTree(Sprite):
	type = "tree"
	def __init__(self,model,coords,env):
		self.model = model
		self.coords = coords
		self.isRemove = False
		self.color = env["color"]
		self.growth = 0
		self.energy = 512
		self.fruits = 0
	def physics(self):
		# Photosynthesis/ Metabolism
		self.energy -= 64
		covered = False
		for x in [-1,0,1]:
			for y in [-1,0,1]:
				if x != 0 or y != 0:
					adjsprite = self.model.getGrid(apply(self.coords,[x,y]))
					if adjsprite != None:
						covered = covered or (adjsprite.type == "tree" and adjsprite.growth >= self.growth)
		if not covered:
			self.energy += 128
		# Energy Decision
		if self.energy <= 0:
			if self.growth > 0:
				self.growth -= 1
				self.energy += 64
			self.isRemove = True
		if self.growth >= 8:
			self.growth -= 4
			self.fruits += 2
		if self.energy >= 1024:
			if not getTable(self.model.tiles,self.coords) in ("sand","steppe") or self.growth <= 0:
				self.growth += 1
			self.energy -= 512
		# Physics Scatter
		if self.fruits >= 1:
			if random.randint(0,2) == 1:
				x = random.randint(-3,4)
				y = random.randint(-3,4)
				newcoords = apply(self.coords,[x,y])
				if self.model.isGridFree(newcoords):
					newsprite = SpriteTree(self.model,newcoords,{"color":"fruit"})
					self.model.addSprite(newsprite)
					self.fruits -= 1
		# Perception
		if self.growth >= 1:
			self.color = "tree"
		if self.growth >= 4:
			self.color = "treegrown"
			if self.fruits >= 1:
				self.color = "treefruit"
	def pluck(self):
		self.fruits -= 1
class SpriteHuman(Sprite):
	type = "human"
	def __init__(self,model,coords,env):
		self.model = model
		self.coords = coords
		self.isRemove = False
		self.name = env["name"]
		self.color = env["color"]
		self.energy = 1024
		self.direction = [0,0]
		self.sanity = 0
		self.isHungry = False
		self.goal = [0,0]
		self.age = 0
	def physics(self):
		# Metabolism
		self.energy -= 2
		self.age += 1
		# State
		if self.energy <= 0 or self.age >= 32*40:
			print self.name, "died"
			self.isRemove = True
		if self.energy <= 512:
			self.isHungry = True
		elif self.energy >= 2048:
			self.isHungry = False
		if self.age % 32 == 0:
			print self.name, self.age/32,"happy birthday" 
		if self.energy >= 1536 and self.age in xrange(32*2,32*40):
			x,y = (random.randint(-1,1),random.randint(-1,1))
			newcoords = apply(self.coords,(x,y))
			if self.model.isGridFree(newcoords):
				newsprite = SpriteHuman(self.model,newcoords,{"color":self.color,"name":self.name+"*"})
				self.model.addSprite(newsprite)
				self.energy -= 1024
		# Grasper
		breakloop = False
		for x in [-1,0,1]:
			for y in [-1,0,1]:
				adjsprite = self.model.getGrid(apply(self.coords,[x,y]))
				if adjsprite != None and adjsprite.type == "tree":
					if adjsprite.growth == 0:
						self.energy += adjsprite.energy-256
						adjsprite.isRemove = True
						breakloop = True
					elif adjsprite.type == "tree" and adjsprite.fruits >= 1:
						adjsprite.pluck()
						self.energy += adjsprite.energy-256
						breakloop = True
				if breakloop: break
			if breakloop: break
		# Eye
		dist = -1
		entities = 0
		for x in xrange(-7,8):
			for y in xrange(-7,8):
				if not(x == 0 and y == 0):
					adjsprite = self.model.getGrid(apply(self.coords,[x,y]))
					if adjsprite != None and adjsprite.type == "tree" and adjsprite.growth == 0:
						dx = 0
						dy = 0
						if x != 0: dx = x/abs(x)
						if y != 0: dy = y/abs(y)
						dist = 0
						self.direction = [dx,dy]
						self.goal = [x-dx,y-dy]
						entities += 1
					elif adjsprite != None and adjsprite.type == "tree":
						dx = 0
						dy = 0
						if x != 0: dx = x/abs(x)
						if y != 0: dy = y/abs(y)
						if ((x**2)+(y**2)) < dist or dist == -1:
							dist = ((x**2)+(y**2))
							self.direction = [dx,dy]
							if self.isHungry:
								self.goal = [x-dx,y-dy]
							else: self.goal =[x,y]
							entities += 1
		if not self.model.isGridFree(apply(self.coords,self.direction)):
			self.direction = [random.randint(-1,1),random.randint(-1,1)]
		#Locomotion
		if self.isHungry:
			#print self.direction
			self.model.moveSprite(self,apply(self.coords,self.direction))
			if self.sanity > 16:
				self.direction = [random.randint(-1,1),random.randint(-1,1)]
				self.sanity = 0
			self.sanity += 1
# Dependency: Sprite, SpriteHuman, SpriteTree, SpriteAnimal
class Model(object):
	def __init__(self):
		self.spritelist = []
		self.addspritelist = []
		self.grid = []
		self.night = False
		self.moved = []
		
	def loadTiles(self, size, tiles):
		self.size = size
		self.tiles = tiles
		for xi in xrange(self.size[0]):
			self.grid.append([])
			for yi in xrange(self.size[1]):
				self.grid[xi].append(None)

	def loadSprites(self, spritelist):
		for s in spritelist:
			sprite = None
			if s[0] == "tree":
				sprite = SpriteTree(self,s[1],s[2])
			if s[0] == "human":
				sprite = SpriteHuman(self,s[1],s[2])
			self.addSprite(sprite)

	def addSprite(self,sprite):
		self.setGrid(sprite.coords,sprite)
		self.addspritelist.append(sprite)

	def setGrid(self,coords,value):
		self.grid[coords[0]][coords[1]] = value
		
	def getGrid(self,coords):
		if not bound([0,0],coords,self.size):
			return None
		return self.grid[coords[0]][coords[1]]
		
	def moveSprite(self,sprite,coords):
		self.moved += [sprite.coords]
		if not bound([0,0],coords,self.size):
			return
		if not self.isGridFree(coords):
			return
		self.setGrid(sprite.coords,None)
		self.setGrid(coords,sprite)
		sprite.coords = coords
		
	def isGridFree(self,coords):
		if not bound([0,0],coords,self.size):
			return False
		if getTable(self.tiles,coords) in ("water","dirt"):
			return False
		return self.getGrid(coords) == None
		
	def physics(self,type=None, taxation=0):
		spritelistp = self.spritelist
		if taxation == 1:
			taxation = self.spritelist[:len(self.spritelist)/2]
		elif taxation == 2:
			taxation = self.spritelist[len(self.spritelist)/2:]
		entities = 0
		for sprite in spritelistp:
			if sprite.type == type or type == None:
				sprite.physics()
				entities += 1
		if type=="human": print entities
		self.spritelist.extend(self.addspritelist)
		self.addspritelist = []
		it = 0
		length = len(self.spritelist)
		while it != length:
			currentsprite = self.spritelist[it]
			if currentsprite.isRemove:
				self.setGrid(currentsprite.coords,None)
				self.moved += [currentsprite.coords]
				del(self.spritelist[it])
				length -= 1
			else:
				it += 1