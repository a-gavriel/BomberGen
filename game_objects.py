import pygame
import time



class GameObject:
	def __init__(self, i, j, scale):
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
	def __init__(self, i, j, scale, matrix = []):
		super().__init__(i,j,scale)
		self.dir_ = 0
		self.matrix = matrix
		self.clear_around(self.matrix)
		self.det_time = 20
		self.timeout = 0
		self.bomb = None
		
	def player_move(self, new_dir, game_matrix):
		self.dir_ = new_dir
		self.move(new_dir, game_matrix)
		'''
		if new_dir == self.dir_:
			self.move(new_dir, game_matrix)
		else:
			self.dir_ = new_dir
		'''
		
	
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
		if self.bomb:
			time_exploding = (self.bomb.timestamp_placed_bomb + self.bomb.duration) 
			time_now = time.time()
			if time_exploding < time_now:
				self.bomb.explode(self.matrix)
				self.bomb = None

	def place_bomb(self, duration = 3):
		if not self.bomb:			
			self.bomb = Bomb(self.i,self.j, self.scale, duration= duration)

	def render(self, gameDisplay):
		super().render(gameDisplay)
		if self.bomb:
			self.bomb.render(gameDisplay)
	

		
class Bomb(GameObject):
	def __init__(self, i, j, map_scale, size = 2, duration = 3):
		self.map_scale = map_scale		
		self.bombsizes = {0:map_scale, 1:(map_scale)//4, 2:map_scale//2, 3:(map_scale*3)//4}
		super().__init__(i,j,self.bombsizes.get(size, map_scale))		
		self.color = (0,0,0)
		self.duration = duration
		self.timestamp_placed_bomb = time.time()

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
		

	def render(self, gameDisplay):
		offset = (self.map_scale - self.scale)//2

		rect = pygame.rect.Rect((self.j * self.map_scale + offset, self.i*self.map_scale + offset, self.scale, self.scale))
		pygame.draw.rect(gameDisplay,self.color,rect)



if __name__ == "__main__":
	raise Exception('--- Please run main.py ---')