"""
    Title: Snake -Simple Version. Basic game using pygame
    Author: Muhammed Enes Koroglu
    Project Start: 5 Sep 2020
    Last Edit: 23 Aug 2021
"""
# import pygame  # is imported by default by Inits.
from Inits import *
import Snake
import Level


class Game:

	def __init__(self, arcade_mode_on=True):
		self.arcade_mode_on = arcade_mode_on
		file = open(FILE_PATH + "highscore.txt", "r")
		self.highscore = int(file.read())
		file.close()

		self.reset()
		self.game_loop()

	def reset(self):
		# Load background music.
		pygame.mixer.music.load(FILE_PATH + 'audio_files\\snake_bg_2.mp3')
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(0.5)

		# Initialize variables.
		self.levels = initialize_levels()  # is not used if self.arcade_mode_on
		self.completed = False
		self.level_index = 0
		self.score = 0
		self.install_level()
		self.paused = False

	def install_level(self):
		self.level_just_started = True
		self.level = self.levels[self.level_index] if not self.arcade_mode_on else Level.Level.get_random_level(
			20 + 2 * self.level_index)
		self.score = 0 if not self.arcade_mode_on else self.score
		self.snake = Snake.Snake(walls=self.level.walls)
		self.manually_moved = False
		self.time_until_move = 1 / SPEED

	def move_if_not_yet_moved(self):
		if self.manually_moved or self.paused:
			self.time_until_move = 1 / SPEED
			self.manually_moved = False
		else:
			if self.time_until_move <= 0:
				self.snake.move(self.snake.direction)
				self.time_until_move = 1 / SPEED
			else:
				self.time_until_move -= 1

	def check_events(self):
		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				pygame.quit()
				quit()
			# Move checks:
			if ev.type == pygame.KEYDOWN and not self.paused:
				self.manually_moved = True
				self.time_until_move = 1 / SPEED
				if ev.key == pygame.K_LEFT or ev.key == pygame.K_k:
					if self.snake.direction != (1, 0):
						self.snake.move((-1, 0))
				if ev.key == pygame.K_RIGHT or ev.key == pygame.K_SEMICOLON:
					if self.snake.direction != (-1, 0):
						self.snake.move((1, 0))
				if ev.key == pygame.K_DOWN or ev.key == pygame.K_l:
					if self.snake.direction != (0, -1):
						self.snake.move((0, 1))
				if ev.key == pygame.K_UP or ev.key == pygame.K_o:
					if self.snake.direction != (0, 1):
						self.snake.move((0, -1))
				if ev.key == pygame.K_ESCAPE:
					self.paused = True
				if ev.key == pygame.K_F11:  # exit full-screen mode.
					pygame.display.set_mode((WINDOW_WIDTH * UNIT, WINDOW_HEIGHT * UNIT), pygame.RESIZABLE)
			elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
				self.paused = False

	def redraw_game_window(self):
		window.fill(BLACK)
		self.snake.draw(window)
		self.level.draw()

		# score
		score_text = FAT_FONT.render('Score: ' + str(self.score) + "/" + str(self.highscore), 1, WHITE)
		window.blit(score_text, ((WINDOW_WIDTH - 6) * UNIT, UNIT))
		# peripheral line
		pygame.draw.rect(window, RED,
						 (0, 0, WINDOW_WIDTH * UNIT, WINDOW_HEIGHT * UNIT), 3)

		if self.paused:
			self.add_semi_transparent_surface()
			text = SLIM_FONT.render('Press ESC to continue', 1, WHITE)
			window.blit(text, (WINDOW_WIDTH // 2 * UNIT - text.get_rect().width // 2,
							   WINDOW_HEIGHT // 2 * UNIT - text.get_rect().height // 2))

		pygame.display.update()
		if self.level_just_started:
			self.wait_for_level_to_start()

	def check_collisions(self):

		self.snake.is_alive = not pos_out_of_bounds(self.snake.positions[0])
		if self.snake.food_pos in self.snake.positions:
			self.snake.eat_food(self.level.walls)
			self.score += 1
		elif self.snake.is_biting_itself():
			self.snake.is_alive = False
		elif self.snake.positions[0] in self.level.walls:
			self.snake.is_alive = False

	def check_lvl_clear(self):
		if not self.arcade_mode_on:  # level clear
			if self.score == self.level.target_score:
				self.level_index += 1
				if self.level_index >= len(self.levels):
					self.game_complete()
				self.install_level()
		elif self.score == (self.level_index + 1) * self.level.target_score:
			self.level_index += 1
			self.install_level()

	def add_semi_transparent_surface(self):
		s = pygame.Surface((WINDOW_WIDTH * UNIT, WINDOW_HEIGHT * UNIT))  # the size of your rect
		s.set_alpha(125)  # alpha level
		s.fill(BLACK)
		window.blit(s, (0, 0))

	def game_over(self):
		pygame.mixer.music.stop()

		# Add texts.
		game_over_text = SLIM_FONT.render('Mission Failed, Wanna try again?', 1, WHITE)
		window.blit(game_over_text, (WINDOW_WIDTH // 2 * UNIT - game_over_text.get_rect().width // 2,
									 WINDOW_HEIGHT // 2 * UNIT - game_over_text.get_rect().height // 2))
		try_again_text = VERY_SLIM_FONT.render('Press UP arrow key to try again', 1, WHITE)
		window.blit(try_again_text, (WINDOW_WIDTH // 2 * UNIT - try_again_text.get_rect().width // 2,
									 WINDOW_HEIGHT // 2 * UNIT + game_over_text.get_rect().height // 2 + try_again_text.get_rect().height // 2))
		give_up_text = VERY_SLIM_FONT.render('or ESC to give up..', 1, WHITE)
		window.blit(give_up_text, (WINDOW_WIDTH // 2 * UNIT - give_up_text.get_rect().width // 2,
								   WINDOW_HEIGHT // 2 * UNIT + game_over_text.get_rect().height // 2 +
								   try_again_text.get_rect().height + give_up_text.get_rect().height // 2))

		# Screen update and game over music
		pygame.display.update()
		pygame.time.delay(300)
		pygame.mixer.music.load(FILE_PATH + 'audio_files\\game_over.mp3')
		pygame.mixer.music.play()
		pygame.mixer.music.set_volume(0.5)

		# Restart for UP-key, exit for ESC
		start_time = pygame.time.get_ticks()
		while pygame.time.get_ticks() - start_time <= 10000:
			for ev in pygame.event.get():
				if ev.type == pygame.KEYDOWN:
					if ev.key == pygame.K_UP or ev.key == pygame.K_o:
						pygame.mixer.music.stop()
						self.reset()
						self.game_loop()
					elif ev.key == pygame.K_ESCAPE:
						return

	def game_complete(self):
		self.completed = True
		self.add_semi_transparent_surface()

		# Add texts.
		you_won_text = SLIM_FONT.render('Congrats!! You\'ve beaten me! I\'ll get you next time ;)', 1, YELLOW)
		window.blit(you_won_text, (WINDOW_WIDTH // 2 * UNIT - you_won_text.get_rect().width // 2,
								   WINDOW_HEIGHT // 2 * UNIT - you_won_text.get_rect().height // 2))
		press_to_exit_text = VERY_SLIM_FONT.render('Press SPACE to complete', 1, WHITE)
		window.blit(press_to_exit_text, (WINDOW_WIDTH // 2 * UNIT - press_to_exit_text.get_rect().width // 2,
										 WINDOW_HEIGHT // 2 * UNIT + you_won_text.get_rect().height // 2 + press_to_exit_text.get_rect().height // 2))

		# Screen update and game complete music
		pygame.display.update()
		pygame.time.delay(300)
		pygame.mixer.music.load(FILE_PATH + 'audio_files\\you_won.mp3')
		pygame.mixer.music.play()
		pygame.mixer.music.set_volume(0.5)

		# ENTER to exit
		while True:
			for ev in pygame.event.get():
				if ev.key == pygame.K_RETURN:
					return

	def wait_for_level_to_start(self):
		self.add_semi_transparent_surface()
		you_won_text = FAT_FONT.render('LVL ' + str(self.level_index + 1), 1, YELLOW)
		window.blit(you_won_text, (WINDOW_WIDTH // 2 * UNIT - you_won_text.get_rect().width // 2,
								   WINDOW_HEIGHT // 2 * UNIT - you_won_text.get_rect().height // 2))
		pygame.display.update()
		pygame.time.wait(2000 + 0 if self.level_index == 0 else 1000)
		for _ in pygame.event.get():
			pass
		self.level_just_started = False

	def check_for_highscore(self):
		if self.score > self.highscore:
			file = open(FILE_PATH + "highscore.txt", "w")
			file.write(str(self.score))
			file.close()

			highscore_text = FAT_FONT.render("High Score beaten! New highscore: " + str(self.score), 1, YELLOW)
			window.blit(highscore_text, (WINDOW_WIDTH // 2 * UNIT - highscore_text.get_rect().width // 2,
										 WINDOW_HEIGHT // 3 * UNIT - highscore_text.get_rect().height // 2))

	def game_loop(self):
		while self.snake.is_alive and not self.completed:
			pygame.time.Clock().tick(FPS)

			self.check_events()
			self.move_if_not_yet_moved()

			self.check_collisions()
			self.check_lvl_clear()

			self.redraw_game_window()

			if not self.snake.is_alive and not self.completed:
				if self.arcade_mode_on: self.check_for_highscore()
				self.game_over()

		pygame.quit()


def initialize_levels():
	lvls = []

	# LVL 1
	lvls.append(Level.Level.get_random_level(20))

	# LVL 2
	cage_begin = (WINDOW_WIDTH * 1 // 4, WINDOW_HEIGHT * 1 // 4)
	cage_end = (WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT * 3 // 4)

	walls = Level.Level.create_cage(cage_begin, cage_end)  # Cage
	walls.update(Level.Level.get_random_pos_4_walls(walls, 7))  # Random Walls
	walls.difference_update(Level.Level.make_doors_on_cage(cage_begin, cage_end))  # Doors on Cage

	lvls.append(Level.Level(walls=walls, wall_color=YELLOW, target_score=20))

	return lvls


if __name__ == "__main__":
	game = Game(arcade_mode_on=True)
