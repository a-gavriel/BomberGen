from typing import Sequence
import pygame
import time

class GameObject:
	"""
	This is the basic GameObject class to be 
	used as a parent to inherit from.
	
	"""
	def __init__(self, i: int, j: int, scale : int):
		self.dir_ : int = 0
		self.i : int = i
		self.j : int = j
		self.w : int = scale
		self.h : int = scale
		self.scale : int = scale
		self.color : tuple = (255,255,0)


	def update(self) -> None:
		print(f'Current pos ({self.i},{self.j})')

		
	def render(self, gameDisplay : pygame.Surface) -> None:
		rect = pygame.rect.Rect((self.j * self.scale, self.i*self.scale, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color,rect)


	def move(self, dir_ : int, mat : list) -> None:
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



	def __init__(self, i : int, j : int, scale : int, matrix : list = [], player_id : int = 0):
		super().__init__(i,j,scale)
		self.alive : bool = True
		self.player_id : int = player_id
		#self.matrix = matrix
		self.clear_around(matrix)
		self.det_time : int = 20
		self.timeout : int = 0
		self.bomb_placed : bool = False

		player_colors : dict = {
			0: (255, 255, 0),
			1: (0	 , 0, 255)	
		}



		self.color : tuple = player_colors[player_id]
		
	def clear_around(self, matrix : list) -> None:
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
		pass

	def render(self, gameDisplay : pygame.Surface) -> None:
		super().render(gameDisplay)

	

		
class Bomb(GameObject):
	bomb_colors = {
			0: (50,50,50),
			1: (0,0,150),
			2: (0,150,0),
			3: (150,0,0)
		}
	bomb_scales = {
		0: 0.25,
		1: 0.5,
		2: 0.75,
		3: 1.0
	}


	def __init__(self, i : int, j : int, map_scale : int, size : int = 0, duration : int = 3, owner : int = 0):
		self.owner : int = owner
		self.map_scale : int = map_scale
		self.bomb_type : int = size	
		super().__init__(i, j, int(Bomb.bomb_scales[size]*map_scale))		
		self.color : tuple = Bomb.bomb_colors[size]
		self.duration : int = duration
		self.timestamp_placed_bomb : float = time.time()
		self.time_exploding : float = (self.timestamp_placed_bomb + self.duration)

	def explode(self, matrix : list) -> None:
		print(f"Bomb exploding in {self.i},{self.j}")
		
		radius = self.bomb_type
		i = self.i
		j = self.j
		m = len(matrix)
		n = len(matrix[0])


		if radius > 0:
			for i in range(self.i - radius, self.i + radius + 1):
				for j in range(self.j - radius, self.j + radius + 1):
					if (0 <= i < m) and (0 <= j < n) and (matrix[i][j] == 1):
						matrix[i][j] = 0

		if radius % 2 == 0:
			pad = radius + 1
			extra_tiles = [(self.i - pad, self.j), 
							(self.i + pad, self.j),
							(self.i, self.j - pad),
							(self.i, self.j + pad)]
			for i,j in extra_tiles:
				if (0 <= i < m) and (0 <= j < n) and (matrix[i][j] == 1):
					matrix[i][j] = 0



	def update(self, matrix : list) -> None:
			time_now = time.time()
			if self.time_exploding < time_now:
				self.explode(matrix)
				return 1
			else:
				return 0

	def render(self, gameDisplay : pygame.Surface) -> None:
		offset = (self.map_scale - self.scale)//2
		rect = pygame.rect.Rect((self.j * self.map_scale + offset, self.i*self.map_scale + offset, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color,rect)

	def render_explosion(gameDisplay : pygame.Surface, i : int , j : int, size : int, map_scale : int) -> None:
		color_4 = *(Bomb.bomb_colors[size]), 127
		surface_length = int(map_scale*1.5)
		if size == 1:
			surface_length = map_scale * 2
		if size == 2:
			surface_length = map_scale * 4
		map_scale_half = map_scale // 2
		rect = (j*map_scale + map_scale_half - surface_length//2, i*map_scale + map_scale_half - surface_length//2, surface_length, surface_length)
		shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
		pygame.draw.rect(shape_surf, color_4, shape_surf.get_rect())
		gameDisplay.blit(shape_surf, rect)

if __name__ == "__main__":
	raise Exception('--- Please run main.py ---')