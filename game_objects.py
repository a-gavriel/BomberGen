from typing import Sequence
from xmlrpc.client import Boolean
import pygame
import time
from utils import *


class GameObject:
	
	def __init__(self, i: int, j: int, scale : int):
		"""
		This is the basic GameObject class to be 
		used as a parent to inherit from. 
		
		<i>: position in the Y axis

		<j>: position in the X axis

		<scale>: size of the object in each 
		dimention. Used for rendering
		
		default color will be set to Yellow

		"""
		self.dir_ : int = 0
		self.i : int = i
		self.j : int = j
		self.w : int = scale
		self.h : int = scale
		self.scale : int = scale
		self.color : tuple = (255,255,0) # Default color


	def update(self) -> None:
		"""
		Default update function will only print the object coordinates
		"""
		print(f'Current pos ({self.i},{self.j})')

		
	def render(self, gameDisplay : pygame.Surface) -> None:
		"""
		Default render will draw a rectange of sides <scale> in (j,i).
		"""

		rect = pygame.rect.Rect((self.j * self.scale, self.i*self.scale, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color.value,rect)


	def move(self, dir_ : int, mat : list) -> None:
		"""
		Default move will move the object to 1 space 
		of the provided direction <dir_> in the 
		matrix <mat> given.

		dir_:
			0:	up
			1:	down
			2:	left
			3:	right

		"""

		self.dir_ = dir_
		#print(f'Current pos ({self.i},{self.j})')
		di = {0:-1, 1:1, 2:0, 3:0}
		dj = {0:0,1:0, 2:-1, 3:1}
		new_i, new_j = self.i + di[dir_] , self.j + dj[dir_]

		if (len(mat) > new_i) and (new_i >= 0) and \
			(len(mat[0]) > new_j) and (new_j >= 0):
			if not (mat[new_i][new_j]):
				self.i = new_i
				self.j = new_j
		else:
			print('Out of bounds!')



class Player(GameObject):

	player_colors : dict = {
		0: Color.RED_1,
		1: Color.GREEN_1,
		2: Color.BLUE_1
	}

	def __init__(self, i : int, j : int, scale : int, matrix : list = [], player_id : int = 0):
		super().__init__(i,j,scale)
		self.alive : bool = True
		self.player_id : int = player_id
		#self.matrix = matrix
		self.clear_around(matrix)
		self.det_time : int = 20
		self.timeout : int = 0
		self.bomb_placed : bool = False


		self.color : tuple = Player.player_colors[player_id]
		
	def clear_around(self, matrix : list) -> None:
		"""
		Clear all the blocks in the matrix where the Player is
		located and in the surrounding ortogonal spaces.
		
		"""

		i = self.i
		j = self.j
		matrix[i][j] = 0
		if matrix[i-1][j] == 1:
			matrix[i-1][j] = 0
		if matrix[i+1][j] == 1:
			matrix[i+1][j] = 0
		if matrix[i][j-1] == 1:
			matrix[i][j-1] = 0
		if matrix[i][j+1] == 1:
			matrix[i][j+1] = 0

	def update(self) -> None:
		"""
		#! No code yet
		"""
		pass

	def render(self, gameDisplay : pygame.Surface) -> None:
		"""
		Renders the Player over the <gameDisplay>.
		# TODO: Update for image
		"""
		super().render(gameDisplay)

	

		
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


	def explode(self, matrix : list, player_list : list[Player]) -> None:
		"""
		Explode the Bomb in the matrix by using the algorithm 
		depending on the bomb type. 

		bomb_type == 0: Destroy all tiles around the bomb. (if possible)

		bomb_type == 2: Destroy the next tile in all directions perpendicular to the bomb.
		"""


		print(f"Bomb exploding in {self.i},{self.j}")
		
		self.time_when_exploded = time.time()

		bomb_type = self.bomb_type
		m = len(matrix)
		n = len(matrix[0])

		players_hit = []


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
			
			



	def update(self) -> Boolean:
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

			
			







		

if __name__ == "__main__":
	raise Exception('--- Please run main.py ---')