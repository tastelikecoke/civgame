import random
import pygame

BLACK = pygame.Color(0,0,0)
GRAY = pygame.Color(127,127,127)
BLUE = pygame.Color(0,0,255)

def apply(l,m):
	i = 0
	n = []
	while i != len(l):
		n += [l[i] + m[i]]
		i += 1
	return n
def applyColor(l,m):
	i = 0
	n = []
	while i != len(l):
		ni = l[i] + m[i]
		if ni < 0:
			ni = 0
		n += [ni]
		i += 1
	return n
def applyFactor(l,m):
	i = 0
	n = []
	while i != len(l):
		n.append((l[i] * m))
		i += 1
	return n
def listequal(l,m):
	i = 0
	n = True
	while i != len(l):
		n = n and (l[i] == m[i])
		i += 1
	return n
def bound(l,m,n):
	return l[0] <= m[0] and m[0] < n[0] and l[1] <= m[1] and m[1] < n[1]

def randcover(x):
	return random.randint((-x),x)
	
def setTable(table,(x,y),value):
	table[x][y] = value
def getTable(table,(x,y)):
	return table[x][y]
def average(list):
	if list == []:
		return 0.0
	else:
		return sum(list) / len(list)