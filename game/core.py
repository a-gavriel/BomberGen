import pygame
import random
import time
from typing import Sequence
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder	

from objects.player import Player
from objects.bomb import Bomb
from utils.colors import Color


class Game:

	NO_BLOCK = 0	
	DESTRUCTIBLE_BLOCK = 1
	INDESTRUCTIBLE_BLOCK = 2
	BORDER_BLOCK = 3

	def __init__(self, past_player_stats = None):
		pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
		self.my_font = pygame.font.SysFont('Arial', 25)

		

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

		if past_player_stats is not None:
			for i, stat in enumerate(past_player_stats):
				self.players[i].victories = stat
				
		self.game_height : int = self.m * self.scale
		self.game_width : int = self.n * self.scale
		self.stats_display_height = self.scale

		self.game_stats_display : pygame.Surface = pygame.Surface((self.game_width, self.stats_display_height))
		self.game_display : pygame.Surface = pygame.Surface((self.game_width,self.game_height))
		self.full_display : pygame.Surface = pygame.display.set_mode((self.game_width,self.game_height + self.stats_display_height))
		self.colors = {
			0: Color.WHITE.value ,
			1: Color.RED.value,
			2: Color.GREY_HALF.value,
			3: Color.GREY_DARK.value
		}
		self.explosion_animations : list[Bomb] = []

	def check_winner(self) -> int:
		"""
		Checks if there is a winner by checking if there is only 1 player left.
		Return -1 if no winner
		Returns player_id if there is a winner
		"""
		one_player_alive = -1
		for player in self.players:
			if player.alive == True:
				if one_player_alive != -1:
					return -1
				else:
					one_player_alive = player.player_id

		return one_player_alive


	def add_players(self, new_player_id : int = 0) -> None:
		"""
		Adds a new player to the players list
		"""
		if len(self.players) >= 4:
			raise Exception("Can't create player, there should not be more than 4 players")

		if new_player_id == 0: # If no player_id is given, set it to the next one not assigned
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
		"""
		Checks if the given player is alive
		"""
		if len(self.players) <= player_number:
			return False
		return self.players[player_number].alive

	def keystroke(self, pressed : Sequence[bool] ) -> None:
		"""
		Process the keystrokes pressed in the game, 
		by moving the different players or opening menus, etc
		"""
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
		"""
		Creates the different types of blocks in the map, 
		border, indestructible and destructible blocks
		"""
		for i in range(self.m):
			for j in range(self.n):
				if (random.random() < self.blocks_rate):
					self.matrix[i][j] = Game.DESTRUCTIBLE_BLOCK
				if not(j%2 or i%2):
					self.matrix[i][j] = Game.INDESTRUCTIBLE_BLOCK
				if (not(j and i)):
					self.matrix[i][j] = Game.BORDER_BLOCK
				if (i == (self.m -1 )) or (j == (self.n -1)):
					self.matrix[i][j] = Game.BORDER_BLOCK
		
	def update(self) -> None:
		"""
		Update the elements in the game
		"""

		run_alg = False
		if run_alg:
			self.findpath(self.players[0], self.players[1])

		for p in self.players:
			p.update()
		for i, bomb in enumerate(self.bomblist):
			exploded = bomb.update()
			if exploded:
				players_hit : list[Player] = bomb.explode(self.matrix, self.players)
				for p in players_hit:
					p.take_damage()
				self.explosion_animations.append(bomb)
				self.bomblist.pop(i)
				self.players[bomb.owner].bomb_placed = False
		
		winner : int = self.check_winner()
		if winner != -1:
			print(f"Congratulations player {winner}!")
			self.players[winner].victories += 1
			return True
		else:
			return False

	def placebomb(self, player_id : int = 0, type : int = 0 , time : int = 3) -> None:
		"""
		Places a bomb in the game by the player "player_id" with a timeout "time"
		"""
		if not (self.players[player_id].bomb_placed):
			self.players[player_id].bomb_placed = True
			new_bomb = Bomb(self.players[player_id].i, self.players[player_id].j, self.scale, type , duration = time, owner = player_id)
			self.bomblist.append(new_bomb)


	def render_stats(self) -> None:
		"""
		Renders the stats for each player, lives and victories
		"""

		text_to_write = ""
		for i,p in enumerate(self.players):
			text_to_write = f' P{i+1}:{p.lives} / V{p.victories}'
			text_surface = self.my_font.render(text_to_write, False, (255, 255, 255))
			if i == 0:
				self.full_display.blit(text_surface,(0,0))
			elif i == 1:
				self.full_display.blit(text_surface,(self.game_width//4,0))
			elif i == 2: 
				self.full_display.blit(text_surface,(self.game_width//2,0))
			elif i == 3: 
				self.full_display.blit(text_surface,(self.game_width//4*3,0))
	

		
		

		return None


	def render(self) -> None:
		"""
		Renders the elements in the game
		"""
		self.game_display.fill((0,0,0))
		self.full_display.fill((0,0,0))

		for i,row in enumerate(self.matrix):
			for j,e in enumerate(row):
				rect = pygame.rect.Rect((j * self.scale, i*self.scale, self.scale, self.scale))
				pygame.draw.rect(self.game_display,self.colors[e], rect)											

		for p in self.players:
			p.render(self.game_display)
		for b in self.bomblist:
			b.render(self.game_display)


		
		for i, current_bomb in enumerate(self.explosion_animations):
			now = time.time()
			if (current_bomb.time_when_exploded + current_bomb.explosion_duration) < now: # Remove the explosion from the list and don't render it
				self.explosion_animations.pop(i)
			else:
				Bomb.render_explosion(self.game_display, current_bomb, self.scale)
		
		
		self.full_display.blit(self.game_display, (0, self.stats_display_height))
		self.render_stats()
		pygame.display.flip()


	
	def print_matrix(self, mat : list) -> None:
		"""
		Prints the game matrix
		"""
		print("\nstart of matrix\n" )
		for i in (mat):
			print (i)
		print("\nend of matrix\n" )

	def parse_matrix(self) -> None:
		"""
		Converts the matrix values in order to use the pathfinding
		"""
		mat2 = [[0]*self.n for i in range(self.m)]
		for  i in range(self.m):
			for j in range(self.n):
				if (self.matrix[i][j] == Game.DESTRUCTIBLE_BLOCK):
					mat2[i][j] = 4	#Weigth of passing through a block
				elif (self.matrix[i][j] == Game.NO_BLOCK):
					mat2[i][j] = 1	#Smallest value for pathfind
				elif (self.matrix[i][j] == Game.INDESTRUCTIBLE_BLOCK) \
						or (self.matrix[i][j] == Game.BORDER_BLOCK):
					mat2[i][j] = -1	#Blocked path
		return mat2
	
	def findpath(self, start_player : Player, end_player : Player) -> None:
		start_pos = start_player.j, start_player.i
		end_pos = end_player.j, end_player.i
		mat = self.parse_matrix()
		grid = Grid(matrix=mat)

		start = grid.node(start_pos[0], start_pos[1])
		end = grid.node(end_pos[0], end_pos[1])

		finder = AStarFinder()
		path, runs = finder.find_path(start, end, grid)

		print('operations:', runs, 'path length:', len(path))
		print(grid.grid_str(path=path, start=start, end=end))

		return 