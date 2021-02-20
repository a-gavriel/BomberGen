from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder	
import pygame
import random


class Game:
	def __init__(self):
		self.m = 10
		self.n = 20
		self.blocks_rate = 0.5
		self.matrix = [[0]*self.n for i in range(self.m)]
		self.set_map()

	def set_map(self):
		for i in range(self.m):
			for j in range(self.n):
				if (random.random() < self.blocks_rate):
					self.matrix[i][j] = 1
				if not(j%2 or i%2):
					self.matrix[i][j] = 2
				if (not(j and i)):
					self.matrix[i][j] = 3
				if (i == (self.m -1 )) or (j == (self.n -1)):
					self.matrix[i][j] = 3

	def print_matrix(self, mat):
		print("\nstart of matrix\n" )
		for i in (mat):
			print (i)
		print("\nend of matrix\n" )

	def parse_matrix(self):
		mat2 = self.matrix
		for  i in range(self.m):
			for j in range(self.n):
				if (mat2[i][j] < 2):
					mat2[i][j] = 1
				else:
					mat2[i][j] = 0
		return mat2
	
	def findpath(self, matrix, pos_bot, pos_player):
		grid = Grid(matrix=matrix)

		start = grid.node(pos_bot[0], pos_bot[1])
		end = grid.node(pos_player[0], pos_player[1])

		finder = AStarFinder()
		path, runs = finder.find_path(start, end, grid)

		print('operations:', runs, 'path length:', len(path))
		print(grid.grid_str(path=path, start=start, end=end))

	def set_action_list(self):
		#up, down, left, right, do nothing
		action_list = []
		total = 0
		for i in range(0, 5):
			action_list.insert(i, random.random())
			total += action_list[i]
		print(action_list)

		print (total)

		for i in range(0, 5):
			action_list[i] = action_list[i]/total
		print(action_list)
		
		return action_list

	def choose_action(self, action_list):
		#action_list = self.action_list
		action = max(action_list)
		action_pos = action_list.index(action)
		if (action_pos) == 0:
			print ("Move Up")
		if (action_pos) == 1:
			print ("Move Down")
		if (action_pos) == 2:
			print ("Move Left")
		if (action_pos) == 3:
			print ("Move Right")
		else:
			print ("Do Nothing")

	def set_accum_prob_list(self):
		accum = 0
		accum_problist = []
		#for i in range(0, 5):
			#
		return 0


game = Game()
game.print_matrix(game.matrix)
game.print_matrix(game.parse_matrix())
game.findpath(game.parse_matrix(), (1,1), (11,8))
game.choose_action(game.set_action_list())


#se tiene un jugador en pos x y compu en pos y 

#acciones
#moverse(4), nada, bomba

#cromosona lista de probabilidad de acciones, esa prob es random 

#para el fitness> que tan cerca estoy del jugador pos bot
				#que tan cerca esta mi bomba del jugador pos bomba = pos_bot
				#pos jugador

#entre mas cerca este de 0 mejor 



#cual es la mejor solucion



