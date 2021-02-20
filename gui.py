import pygame
import main

class Player:
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.det_time = 20
		self.timeout = 0
	
	def update(self):
		if self.timeout > 0:
			self.timeout -= 1
	def place_bomb(self):
		pass

	def move(self,dir_, mat):
		di = {0:-1, 1:1, 2:0, 3:0}
		dj = {0:0,1:0, 2:-1, 3:1}
		new_i, new_j = self.i + di[dir_] , self.j + dj[dir_]

		if not (mat[new_i][new_j]):
			self.i = new_i
			self.j = new_j
		


		pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_LEFT]:
      player.move(2,game.matrix)
    if pressed[pygame.K_RIGHT]:
      player.move(3,game.matrix)
    if pressed[pygame.K_UP]:
      player.move(0,game.matrix)
    if pressed[pygame.K_DOWN]:
      player.move(1,game.matrix)
    if pressed[pygame.K_SPACE]:
			print(" game.placebomb(player) ")



