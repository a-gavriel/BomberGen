import pygame
import time
from game.core import Game

def run() -> None:
	pygame.init()
	clock =	pygame.time.Clock()
	game_is_playing = True

	player_stats : list = None
	while game_is_playing:
		crash = False
		game = Game(player_stats)
		#game.print_matrix(game.matrix)
		#game.print_matrix(game.parse_matrix())
		#game.findpath(game.parse_matrix(), (1,1), (11,8))
		exiting_game : bool = False
		finishing_animations : bool = False
		finishing_animations_timer : float = 0.0
		while not crash:
			if not exiting_game:
				exiting_game = game.update()
			else:
				if not finishing_animations:
					finishing_animations = True
					finishing_animations_timer = time.time() + 2.0
				if finishing_animations and (finishing_animations_timer < time.time()):
					player_stats = []
					for p in game.players:
						player_stats.append(p.victories)

					crash = True
					if max(player_stats) == 3:
						game_is_playing = False

					

			game.render()
			for event in pygame.event.get():
					if event.type == pygame.QUIT:						
							crash = True
							
			pressed = pygame.key.get_pressed()		
			game.keystroke(pressed)
			clock.tick(10)
	pygame.quit()
run()

