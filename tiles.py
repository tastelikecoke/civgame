import pickle
import random
import pygame
from game_modules import *

def diamondSquare(heightsize):
	heights = []
	for i in xrange(heightsize + 1):
		heights += [[]]
		for j in xrange(heightsize + 1):
			heights[i] += [0.0]
	squaresize = heightsize/2
	heights[heightsize/2][heightsize/2] = 1.0
	r = 1.0
	while squaresize != 1:
		x = squaresize/2
		while x < heightsize:
			y = squaresize/2
			while y  < heightsize:
				heightlist = []
				for dx in [-1,1]:
					for dy in [-1,1]:
						xp = x + dx*squaresize/2
						yp = y + dy*squaresize/2
						heightlist += [heights[xp][yp]]
				meanheight = average(heightlist)
				meanheight += random.uniform(-r,r)
				setTable(heights,(x,y),meanheight)
				y += squaresize
			x += squaresize
		x = 0
		isOdd = True
		while x < heightsize:
			y = 0
			if isOdd: y += squaresize/2
			while y < heightsize:
				heightlist = []
				for dx in [-1,0,1]:
					for dy in [-1,0,1]:
						if (dx == 0) != (dy == 0): # XOR
							xp = x + dx*squaresize/2
							yp = y + dy*squaresize/2
							if bound((0,0),(xp,yp),(heightsize+1,heightsize+1)):
								heightlist += [heights[xp][yp]]
				if meanheight == [] : print "empty"
				meanheight = average(heightlist)
				meanheight += random.uniform(-r,r) 
				setTable(heights,(x,y),meanheight)
				y += squaresize
			x += squaresize/2
			isOdd = not isOdd
		squaresize /= 2
		r /= 2
	return heights

def addCone(heights, heightsize):
	for i in xrange(heightsize):
		for j in xrange(heightsize):
			dist = (i-heightsize/2)**2 + (j-heightsize/2)**2
			heights[i][j] += -dist/((64.0**2)*2.0)

def getAverageHeight(heights):
	averages = []
	for row in heights:
		averages += [average(row)]
	return average(averages)

random.seed()
tiles = []
size = [128,128]
colordict = {"grass":(0,192,0),
	"dirt":(144,128,0),
	"steppe":(128,192,0),
	"sand":(216,255,0),
	"water":(0,0,255)}

heights = diamondSquare(128)
addCone(heights,128)
sealevel = getAverageHeight(heights)

for i in xrange(size[0]):
	tiles += [[]]
	for j in xrange(size[1]):
		if heights[i][j] > 1.2+sealevel:
			tiles[i] += ["dirt"]
		elif heights[i][j] > 1.0+sealevel:
			tiles[i] += ["steppe"]
		elif heights[i][j] > 0.2+sealevel:
			tiles[i] += ["grass"]
		elif heights[i][j] > 0.0+sealevel:
			tiles[i] += ["sand"]
		else:
			tiles[i] += ["water"]
		
f = open("tiles.game","w")
pickle.dump([size,tiles,16,colordict],f)