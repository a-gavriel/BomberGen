import pygame
from utils.colors import rgb


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
		self.color : tuple = rgb(255,255,0) # Default color


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
		pygame.draw.rect(gameDisplay, self.color.value,rect)


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










		

if __name__ == "__main__":
	raise Exception('--- Please run main.py ---')