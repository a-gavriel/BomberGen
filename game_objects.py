import pygame
import time

class GameObject:
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

		try:
			if not (mat[new_i][new_j]):
				self.i = new_i
				self.j = new_j
		except Exception:
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

	def player_placebomb(self, duration : int = 3):
		if not self.bomb_placed:			
			self.bomb_placed = True
			return Bomb(self.i,self.j, self.scale, duration= duration)
		else:
			return 0

	def render(self, gameDisplay : pygame.Surface) -> None:
		super().render(gameDisplay)

	

		
class Bomb(GameObject):
	def __init__(self, i : int, j : int, map_scale : int, size : int = 2, duration : int = 3, owner : int = 0):
		self.owner : int = owner
		self.map_scale : int = map_scale		
		self.bombsizes : dict = {
			0:map_scale,
			1:(map_scale)//4, 
			2:map_scale//2, 
			3:(map_scale*3)//4
		}
		super().__init__(i,j,self.bombsizes.get(size, map_scale))		
		self.color : tuple = (0,0,0)
		self.duration : int = duration
		self.timestamp_placed_bomb : float = time.time()
		self.time_exploding : float = (self.timestamp_placed_bomb + self.duration)

	def explode(self, matrix : list) -> None:
		print(f"Bomb exploding in {self.i},{self.j}")
		
		i = self.i
		j = self.j
		if matrix[i][j] == 1:
			matrix[i][j] = 0
		if matrix[i-1][j] == 1:
			matrix[i-1][j] = 0
		if matrix[i+1][j] == 1:
			matrix[i+1][j] = 0
		if matrix[i][j-1] == 1:
			matrix[i][j-1] = 0
		if matrix[i][j+1] == 1:
			matrix[i][j+1] = 0
		
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



if __name__ == "__main__":
	raise Exception('--- Please run main.py ---')