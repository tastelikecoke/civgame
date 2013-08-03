import pickle
import pygame

f = open("sprites.game","w")

imagedict = {"tree":"sprite/treeY16.png",
		"treegrown":"sprite/tree16.png",
		"treedecay":"sprite/treeD16.png",
		"fruit":"sprite/fruit16.png",
		"treefruit":"sprite/treeF16.png",
		"humanblue":"sprite/humanD16.png",
		"humanpink":"sprite/humanC16.png"}
list = [
	["tree",[42,80],{"color":"tree"}],
	["human",[44,74],{"color":"humanpink","name":"Shane"}],
	["human",[44,75],{"color":"humanblue","name":"Boxer"}]
	]

pickle.dump([imagedict,list],f)