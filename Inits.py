import pygame
import random

# Constants
YELLOW = (255, 255, 0)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
ORANGE = (255, 125, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UNIT = 25  # i.e. 1 unit is 10 pixels
# or 1 square unit is 10 pixels down and 10 pixels right.
WINDOW_WIDTH = 20  # in UNITs
WINDOW_HEIGHT = 15  # in UNITs
FPS = 60
SPEED = .15  # .1 == comfortable
ALL_SQUARES = set([(x, y) for x in range(WINDOW_WIDTH) for y in range(WINDOW_HEIGHT)])
FILE_PATH = "C:/Users/menes/PycharmProjects/ForFun/Snake/"
# Initialize pygame and the game window
pygame.init()
pygame.display.set_caption('Snake -Simple Version')
window = pygame.display.set_mode((WINDOW_WIDTH * UNIT, WINDOW_HEIGHT * UNIT), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

FAT_FONT = pygame.font.Font(FILE_PATH + 'comicsans-font/Ldfcomicsansbold-zgma.ttf', 25)
SLIM_FONT = pygame.font.Font(FILE_PATH + 'comicsans-font/Ldfcomicsansbold-zgma.ttf', 20)
VERY_SLIM_FONT = pygame.font.Font(FILE_PATH + 'comicsans-font/Ldfcomicsansbold-zgma.ttf', 15)
# FAT_FONT = pygame.font.SysFont('comicsans', 25, bold=False, )
# SLIM_FONT = pygame.font.SysFont('comicsans', 20, bold=False, )
# VERY_SLIM_FONT = pygame.font.SysFont('comicsans', 15, bold=False, )


def pos_out_of_bounds(pos):
	"""
    :param pos: tuple of (x, y)
    """
	return not ((0 <= pos[0] < WINDOW_WIDTH) and (0 <= pos[1] < WINDOW_HEIGHT))


def is_on_horiz_border(portal):
	return (portal[1] == 0 or portal[1] == WINDOW_HEIGHT) and (0 <= portal[0] <= WINDOW_WIDTH)


def is_on_vertical_border(portal):
	return (portal[0] == 0 or portal[0] == WINDOW_WIDTH) and (0 <= portal[1] <= WINDOW_HEIGHT)


def get_random_pos_except(exceptions):
	return random.choice(tuple(ALL_SQUARES - exceptions))


def get_neighbors(pos, exceptions=set()):
	""" Returns neighboring positions that are inside the window boundaries."""
	neighbors = {(pos[0], pos[1] + 1),
				 (pos[0], pos[1] - 1),
				 (pos[0] + 1, pos[1]),
				 (pos[0] - 1, pos[1])}
	return set(filter(lambda n: not pos_out_of_bounds(n) and n not in exceptions, neighbors))


def is_exitable(pos, walls, count=0):
	neighbors = get_neighbors(pos, walls)
	if count == 0:
		return len(neighbors) >= 2

	# For some reason the code below doesn't check its neighbors' exitability properly.
	# for n in neighbors:
	# 	if not is_exitable(n, walls, count - 1):
	# 		return False
	return True
