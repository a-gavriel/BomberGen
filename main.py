from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder	
import pygame
import random


class Game:
	def __init__(self):
		self.m = 11
		self.n = 21
		self.blocks_rate = 0.5
		self.matrix = [[0]*self.n for i in range(self.m)]
		self.set_map()

		self.player = (self.m//2 , self.n-2)
		self.bot = (self.m//2 , 1)

		self.scale = 40

		self.game_height = self.m * self.scale
		self.game_width =self.n * self.scale
		self.gameDisplay = pygame.display.set_mode((self.game_width,self.game_height))
		self.colors = {
			0:(255,255,255),
			1:(255,0,0),
			2:(0,0,255),
			3:(0,255,0)}

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

		# player and bot initial positions
		self.matrix[self.m//2][self.n-2] = 0
		self.matrix[self.m//2][1] = 0
		
	
	def render(self):

		self.gameDisplay.fill((0,0,0))
		for i,row in enumerate(self.matrix):
			for j,e in enumerate(row):
				rect = pygame.rect.Rect((j * self.scale, i*self.scale, self.scale, self.scale))
				pygame.draw.rect(self.gameDisplay,self.colors[e],rect)
				a = pygame.rect.Rect((i * self.scale, i*self.scale, self.scale/2, self.scale/2))
				pygame.draw.rect(self.gameDisplay,self.colors[e],a)
				pygame.draw.rect(self.gameDisplay,self.colors[e],rect)
		pygame.display.flip()


	

	def print_matrix(self, mat):
		print("\nstart of matrix\n" )
		for i in (mat):
			print (i)
		print("\nend of matrix\n" )
	def parse_matrix(self):
		mat2 = [[0]*self.n for i in range(self.m)]
		for  i in range(self.m):
			for j in range(self.n):
				if (self.matrix[i][j] < 2):
					mat2[i][j] = 1
				else:
					mat2[i][j] = 0
		return mat2.copy()
	
	def findpath(self, mat, pos_bot, pos_player):
		grid = Grid(matrix=mat)

		start = grid.node(pos_bot[0], pos_bot[1])
		end = grid.node(pos_player[0], pos_player[1])

		finder = AStarFinder()
		path, runs = finder.find_path(start, end, grid)

		print('operations:', runs, 'path length:', len(path))
		print(grid.grid_str(path=path, start=start, end=end))



def run():
	pygame.init()
	clock =	pygame.time.Clock()
	crash = False
	game = Game()
	game.print_matrix(game.matrix)
	game.print_matrix(game.parse_matrix())
	#game.findpath(game.parse_matrix(), (1,1), (11,8))
	while not crash:
		game.render()
		pygame.event.get()
		print(" new render")
		clock.tick(5)
	pygame.quit()

run()

