from objects.game_objects import GameObject
from utils.colors import Color
import pygame
import time


class Player(GameObject):

	player_colors : dict = {
		0: Color.RED_1,
		1: Color.GREEN_1,
		2: Color.BLUE_1,
		3: Color.PURPLE_1
	}

	def __init__(self, i : int, j : int, scale : int, matrix : list = [], player_id : int = 0):
		super().__init__(i,j,scale)
		self.alive : bool = True
		self.player_id : int = player_id
		self.lives : int = 3
		self.victories : int = 0
		#self.matrix = matrix
		self.clear_around(matrix)
		self.det_time : int = 20
		self.timeout : int = 0
		self.bomb_placed : bool = False
		self.hit_timer : float = 0.0
		self.was_hit : bool = False
		self.hit_animation_duration : float = 0.5


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


	def take_damage(self) -> bool:
		if self.lives <= 0:
			return False
			
		self.lives -= 1
		self.alive = self.lives > 0
		self.was_hit = True
		self.hit_timer = time.time() + self.hit_animation_duration
		print(f"Player {self.player_id} took damage, current lives: {self.lives}")
		return True

	def update(self) -> None:
		"""
		Checks if the hit timer is over
		"""
		if self.was_hit and self.hit_timer < time.time():
			self.was_hit = False
			self.hit_timer = 0.0
			

	def render(self, gameDisplay : pygame.Surface) -> None:
		"""
		Renders the Player over the <gameDisplay> as a circle if it's alive.
		If player is dead renders a small rectangle.
		If player just took damage, renders player with color white intermittently.
		
		"""

		if self.alive:
			radius = self.scale // 2
			center = self.j * self.scale + radius, self.i*self.scale + radius
			SECONDS_TIME_10 = int(time.time() * 10)
			ITERMITENT_RATE = 4
			if self.was_hit and (SECONDS_TIME_10 % ITERMITENT_RATE >= (ITERMITENT_RATE//2)):
				pygame.draw.circle(gameDisplay, Color.WHITE.value, center, radius)	
			else:
				pygame.draw.circle(gameDisplay, self.color.value, center, radius)

		else:			
			offset = self.scale // 2
			offset_half = offset // 2
			rect = pygame.rect.Rect((self.j * self.scale + offset_half, self.i*self.scale + offset, self.scale - offset, self.scale - offset))
			pygame.draw.rect(gameDisplay, self.color.value, rect)

	


