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


game = Game()
game.print_matrix(game.matrix)
game.print_matrix(game.parse_matrix())

