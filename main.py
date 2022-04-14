from typing import Sequence
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder	
import pygame
import random
from game_objects import *

class Game:
	def __init__(self):
		self.m : int = 11
		self.n : int = 21
		self.blocks_rate : float = 0.5
		self.matrix : list = [[0]*self.n for i in range(self.m)]
		self.set_map()
		self.bomblist : list = []
		self.scale : int = 40
		self.players : list[Player] = []
		self.add_players()
		self.add_players()
		self.game_height : int = self.m * self.scale
		self.game_width : int = self.n * self.scale
		self.gameDisplay : pygame.Surface = pygame.display.set_mode((self.game_width,self.game_height))
		self.colors = {
			0:rgb(255,255,255),
			1:rgb(255,0,0),
			2:rgb(150,150,150),
			3:rgb(50,50,50)
		}
		self.explosion_animations : list[Bomb] = []

	def add_players(self, new_player_id : int = 0) -> None:
		if new_player_id == 0:
			new_player_id = len(self.players)

		initial_positions = {
			0: (self.m//2 , self.n-2),
			1: (self.m-2 , self.n//2),
			2: (self.m//2 , 1),
			3: (1 , self.n//2)
		}
		player_x, player_y = initial_positions[new_player_id]
		self.players.append(Player(player_x, player_y, self.scale, self.matrix, player_id = new_player_id))

	def is_player_alive(self, player_number : int) -> bool:
		if len(self.players) <= player_number:
			return False
		return self.players[player_number].alive

	def keystroke(self, pressed : Sequence[bool] ) -> None:

		if self.is_player_alive(0):
			if pressed[pygame.K_a]:
				self.players[0].move(2,self.matrix)
			if pressed[pygame.K_d]:
				self.players[0].move(3,self.matrix)
			if pressed[pygame.K_w]:
				self.players[0].move(0,self.matrix)
			if pressed[pygame.K_s]:
				self.players[0].move(1,self.matrix)
			#if pressed[pygame.K_SPACE]:
			#	self.placebomb(player_id = 0, time = 3)
			if pressed[pygame.K_1]:
				self.placebomb(player_id = 0, type = 0, time = 1)
			if pressed[pygame.K_2]:
				self.placebomb(player_id = 0, type = 0, time = 2)
			if pressed[pygame.K_3]:
				self.placebomb(player_id = 0, type = 2, time = 3)

		if self.is_player_alive(1):
			if pressed[pygame.K_LEFT]:
				self.players[1].move(2,self.matrix)
			if pressed[pygame.K_RIGHT]:
				self.players[1].move(3,self.matrix)
			if pressed[pygame.K_UP]:
				self.players[1].move(0,self.matrix)
			if pressed[pygame.K_DOWN]:
				self.players[1].move(1,self.matrix)
			if pressed[pygame.K_KP1]:
				self.placebomb(player_id = 1, type = 0, time = 1)
			if pressed[pygame.K_KP2]:
				self.placebomb(player_id = 1, type = 0, time = 2)
			if pressed[pygame.K_KP3]:
				self.placebomb(player_id = 1, type = 2, time = 3)

	
	def set_map(self) -> None:
		# Creates the different types of blocks in the map, border, indestructible and destructible blocks
		for i in range(self.m):
			for j in range(self.n):
				if (random.random() < self.blocks_rate):
					self.matrix[i][j] = 1#destructible 1
				if not(j%2 or i%2):
					self.matrix[i][j] = 2 #indestructible 2 
				if (not(j and i)):
					self.matrix[i][j] = 3 #border 3
				if (i == (self.m -1 )) or (j == (self.n -1)):
					self.matrix[i][j] = 3 #border 3
		
	def update(self) -> None:
		# Update the elements in the game
		for p in self.players:
			p.update()
		for i, bomb in enumerate(self.bomblist):
			exploded = bomb.update()
			if exploded:
				bomb.explode(self.matrix, self.players)
				self.explosion_animations.append(bomb)
				self.bomblist.pop(i)
				self.players[bomb.owner].bomb_placed = False
				

	def placebomb(self, player_id : int = 0, type : int = 0 , time : int = 3) -> None:
		# Places a bomb in the game by the player "player_id" with a timeout "time"
		if not (self.players[player_id].bomb_placed):
			self.players[player_id].bomb_placed = True
			new_bomb = Bomb(self.players[player_id].i, self.players[player_id].j, self.scale, type , duration = time, owner = player_id)
			self.bomblist.append(new_bomb)

	def render(self) -> None:
		# Renders the elements in the game
		self.gameDisplay.fill((0,0,0))
		for i,row in enumerate(self.matrix):
			for j,e in enumerate(row):
				rect = pygame.rect.Rect((j * self.scale, i*self.scale, self.scale, self.scale))
				pygame.draw.rect(self.gameDisplay,self.colors[e],rect)											

		for p in self.players:
			p.render(self.gameDisplay)
		for b in self.bomblist:
			b.render(self.gameDisplay)


		
		for i, current_bomb in enumerate(self.explosion_animations):
			now = time.time()
			if (current_bomb.time_when_exploded + current_bomb.explosion_duration) < now: # Remove the explosion from the list and don't render it
				self.explosion_animations.pop(i)
			else:
				Bomb.render_explosion(self.gameDisplay, current_bomb, self.scale)
		
		pygame.display.flip()

	def draw_rect_alpha(self, surface, color, rect) -> None:
		shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
		pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
		surface.blit(shape_surf, rect)

	# ? Debug 
	def print_matrix(self, mat : list) -> None:
		# Prints the game matrix
		print("\nstart of matrix\n" )
		for i in (mat):
			print (i)
		print("\nend of matrix\n" )

	def parse_matrix(self) -> None:
		# * Converts the matrix values in order to use the pathfinding
		mat2 = [[0]*self.n for i in range(self.m)]
		for  i in range(self.m):
			for j in range(self.n):
				if (self.matrix[i][j] < 2):
					mat2[i][j] = 1
				else:
					mat2[i][j] = 0
		return mat2.copy()
	
	def findpath(self, pos_bot : tuple, pos_player : tuple):
		mat = self.parse_matrix(self.matrix)
		grid = Grid(matrix=mat)

		start = grid.node(pos_bot[0], pos_bot[1])
		end = grid.node(pos_player[0], pos_player[1])

		finder = AStarFinder()
		path, runs = finder.find_path(start, end, grid)

		print('operations:', runs, 'path length:', len(path))
		print(grid.grid_str(path=path, start=start, end=end))



def run() -> None:
	pygame.init()
	clock =	pygame.time.Clock()
	crash = False
	game = Game()
	game.print_matrix(game.matrix)
	game.print_matrix(game.parse_matrix())
	#game.findpath(game.parse_matrix(), (1,1), (11,8))
	while not crash:
		game.update()
		game.render()
		for event in pygame.event.get():
				if event.type == pygame.QUIT:						
						crash = True
						
		pressed = pygame.key.get_pressed()		
		game.keystroke(pressed)
		clock.tick(10)
	pygame.quit()
run()

