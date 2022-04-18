from objects.game_objects import GameObject
from utils.colors import rgb
from objects.player import Player

import time
import pygame

class Bomb(GameObject):
	bomb_colors = {
			0: rgb(50,50,50),
			1: rgb(0,0,150),
			2: rgb(0,150,0),
			3: rgb(150,0,0)
		}
	bomb_scales = {
		0: 0.25,
		1: 0.5,
		2: 0.75,
		3: 1.0
	}


	def __init__(self, i : int, j : int, map_scale : int, bomb_type : int = 0, duration : int = 3, owner : int = 0):
		self.owner : int = owner
		self.map_scale : int = map_scale
		self.bomb_type : int = bomb_type	
		super().__init__(i, j, int(Bomb.bomb_scales[bomb_type]*map_scale))		
		self.color : tuple = Bomb.bomb_colors[bomb_type]
		self.timer_duration : int = duration
		self.time_when_placed : float = time.time()
		self.time_exploding : float = (self.time_when_placed + self.timer_duration)
		self.explosion_duration : float = 0.5
		self.time_when_exploded : float = 0.0
		self.explosion_details : list[int] = []


	def explode(self, matrix : list, player_list : list[Player]) -> list [Player]:
		"""
		Explode the Bomb in the matrix by using the algorithm 
		depending on the bomb type. 

		bomb_type == 0: Destroy all tiles around the bomb. (if possible)

		bomb_type == 2: Destroy the next tile in all directions perpendicular to the bomb.
		"""


		#print(f"Bomb exploding in {self.i},{self.j}")
		
		self.time_when_exploded = time.time()

		bomb_type = self.bomb_type
		m = len(matrix)
		n = len(matrix[0])

		players_hit : list [Player] = []


		if (bomb_type == 0):
			# Destroy any destructible tiles in the corresponding radius
			RADIUS = 1
			for i in range(self.i - RADIUS, self.i + RADIUS + 1):
				for j in range(self.j - RADIUS, self.j + RADIUS + 1):
					if (0 <= i < m) and (0 <= j < n):
						if (matrix[i][j] == 1):
							matrix[i][j] = 0

			# Check if a player is hit by the explosion
			for p in player_list:
				if ((self.i-RADIUS) <= (p.i) <= (self.i+RADIUS)) and ((self.j-RADIUS) <= (p.j) <= (self.j+RADIUS)) and (p not in players_hit):
					players_hit.append(p)
		
		elif bomb_type == 2:

			self.explosion_details.clear


			# Destroy the next block above (if possible)
			for i in range(self.i, -1, -1):
				for p in player_list:
					if (i == p.i) and (self.j == p.j) and (p not in players_hit):
						players_hit.append(p)
				if (matrix[i][self.j] >= 1):
					if (matrix[i][self.j] == 1):
						matrix[i][self.j] = 0
					self.explosion_details.append(i+1)
					#else:
					#	self.explosion_details.append(i+1)
					break
			

			# Destroy the next block below (if possible)
			for i in range(self.i, m, 1):
				for p in player_list:
					if (i == p.i) and (self.j == p.j) and (p not in players_hit):
						players_hit.append(p)
				if (matrix[i][self.j] >= 1):
					if (matrix[i][self.j]) == 1:
						matrix[i][self.j] = 0
					self.explosion_details.append(i)
					#else:
					#	self.explosion_details.append(i)
					break


			# Destroy the next block to the left (if possible)
			for j in range(self.j, -1, -1):
				for p in player_list:
					if (self.i == p.i) and (j == p.j) and (p not in players_hit):
						players_hit.append(p)
				if (matrix[self.i][j] >= 1):
					if (matrix[self.i][j] == 1):
						matrix[self.i][j] = 0
					self.explosion_details.append(j+1)
					#else:
					#	self.explosion_details.append(j+1)
					break
			

			# Destroy the next block to the right (if possible)
			for j in range(self.j, n, 1):
				for p in player_list:
					if (self.i == p.i) and (j == p.j) and (p not in players_hit):
						players_hit.append(p)
				if (matrix[self.i][j] >= 1):
					if (matrix[self.i][j] == 1):
						matrix[self.i][j] = 0
					self.explosion_details.append(j)
					#else:
					#	self.explosion_details.append(j)
					break
			
		return players_hit


	def update(self) -> bool:
			"""
			Check if the bomb should explode, based on the time it was placed and the timeout set to it.
			"""
			time_now = time.time()
			if self.time_exploding < time_now:
				return True
			else:
				return False

	def render(self, gameDisplay : pygame.Surface) -> None:
		"""
		Draw the Bomb
		"""
		offset = (self.map_scale - self.scale)//2
		rect = pygame.rect.Rect((self.j * self.map_scale + offset, self.i*self.map_scale + offset, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color,rect)



	def render_explosion(gameDisplay : pygame.Surface, exploded_bomb : 'Bomb', map_scale : int) -> None:
		"""
		Draws the bomb explosion animation over the surface
		"""
		color_4 = *(Bomb.bomb_colors[exploded_bomb.bomb_type]), 127  # Create a tuple of 4 values reusing the 3 from the bomb colors

		OFFSET = map_scale // 3
		OFFSET_HALF = OFFSET // 2
		SURFACE_LENGTH = map_scale + OFFSET
		

		if (exploded_bomb.bomb_type == 0):
			# Destroy any destructible tiles in the corresponding radius
			rect = (exploded_bomb.j*map_scale - OFFSET_HALF, 
							exploded_bomb.i*map_scale - OFFSET_HALF, 
							SURFACE_LENGTH, SURFACE_LENGTH)
			
			shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
			pygame.draw.rect(shape_surf, color_4, shape_surf.get_rect())
			gameDisplay.blit(shape_surf, rect)

		
		elif (exploded_bomb.bomb_type == 2):
			height_1 = (exploded_bomb.explosion_details[1] - exploded_bomb.explosion_details[0] )*map_scale
			rect_1 = (exploded_bomb.j*map_scale - OFFSET_HALF, 
						exploded_bomb.explosion_details[0]*map_scale - OFFSET_HALF, 
						SURFACE_LENGTH, height_1 + OFFSET)
			
			width_2 = (exploded_bomb.explosion_details[3] - exploded_bomb.explosion_details[2] )*map_scale
			rect_2 = (exploded_bomb.explosion_details[2]*map_scale - OFFSET_HALF, 
						exploded_bomb.i*map_scale - OFFSET_HALF,
						width_2 + OFFSET, SURFACE_LENGTH)
	
			shape_surf = pygame.Surface(pygame.Rect(rect_1).size, pygame.SRCALPHA)
			pygame.draw.rect(shape_surf, color_4, shape_surf.get_rect())
			gameDisplay.blit(shape_surf, rect_1)

			shape_surf = pygame.Surface(pygame.Rect(rect_2).size, pygame.SRCALPHA)
			pygame.draw.rect(shape_surf, color_4, shape_surf.get_rect())
			gameDisplay.blit(shape_surf, rect_2)

			
			