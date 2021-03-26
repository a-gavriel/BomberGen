import pygame

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

class Player(GameObject):
	def __init__(self, i, j, scale, matrix = []):
		super().__init__(i,j,scale)
		self.clear_around(matrix)
		self.det_time = 20
		self.timeout = 0
	
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
		if self.timeout > 0:
			self.timeout -= 1
	def place_bomb(self):
		pass

	def move(self,dir_, mat):
		print(f'Current pos ({self.i},{self.j})')
		di = {0:-1, 1:1, 2:0, 3:0}
		dj = {0:0,1:0, 2:-1, 3:1}
		new_i, new_j = self.i + di[dir_] , self.j + dj[dir_]

		try:
			if not (mat[new_i][new_j]):
				self.i = new_i
				self.j = new_j
		except Exception:
			print('out of bounds')

		



