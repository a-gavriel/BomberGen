import pygame
import time



class GameObject:
	def __init__(self, i, j, scale):
		self.dir_ = 0
		self.i = i
		self.j = j
		self.w = scale
		self.h = scale
		self.scale = scale
		self.color = (255,255,0)		
	def update(self):
		print(f'Current pos ({self.i},{self.j})')
	def render(self, gameDisplay):
		rect = pygame.rect.Rect((self.j * self.scale, self.i*self.scale, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color,rect)


	def move(self,dir_, mat):
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
	def __init__(self, i, j, scale, matrix = [], player_id = 0):
		super().__init__(i,j,scale)
		self.alive = True
		self.player_id = player_id
		#self.matrix = matrix
		self.clear_around(matrix)
		self.det_time = 20
		self.timeout = 0
		self.bomb_placed = False

		player_colors = {
			0: (255, 255, 0),
			1: (0	 , 0, 255)	
		}
		self.color = player_colors[player_id]
		
	def clear_around(self, matrix):
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

	def update(self):
		pass

	def player_placebomb(self, duration = 3):
		if not self.bomb:			
			self.bomb = 1
			return Bomb(self.i,self.j, self.scale, duration= duration)
		else:
			return 0

	def render(self, gameDisplay):
		super().render(gameDisplay)

	

		
class Bomb(GameObject):
	def __init__(self, i, j, map_scale, size = 2, duration = 3, owner = 0):
		self.owner = owner
		self.map_scale = map_scale		
		self.bombsizes = {0:map_scale, 1:(map_scale)//4, 2:map_scale//2, 3:(map_scale*3)//4}
		super().__init__(i,j,self.bombsizes.get(size, map_scale))		
		self.color = (0,0,0)
		self.duration = duration
		self.timestamp_placed_bomb = time.time()
		self.time_exploding = (self.timestamp_placed_bomb + self.duration)

	def explode(self, matrix):
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
		
	def update(self, matrix):
			 
			time_now = time.time()
			if self.time_exploding < time_now:
				self.explode(matrix)
				return 1
			else:
				return 0

	def render(self, gameDisplay):
		offset = (self.map_scale - self.scale)//2

		rect = pygame.rect.Rect((self.j * self.map_scale + offset, self.i*self.map_scale + offset, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color,rect)



if __name__ == "__main__":
	raise Exception('--- Please run main.py ---')