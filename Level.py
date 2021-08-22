from Inits import *


class Level:
    WALL_IMAGE = pygame.image.load(FILE_PATH + 'image_files/wall3.png')

    def __init__(self, portals_horiz=set(), portals_vertical=set(), walls=set(), portal_color=YELLOW, wall_color=WHITE, target_score=40):
        assert all([is_on_horiz_border(portal) for portal in portals_horiz])
        assert all([is_on_vertical_border(portal) for portal in portals_vertical])
        assert all([not pos_out_of_bounds(wall) for wall in walls])

        self.portals_horiz = portals_horiz
        self.portals_vertical = portals_vertical
        self.walls = walls
        self.portal_color = portal_color
        self.wall_color = wall_color
        self.target_score = target_score

    def draw(self):
        for portal_horiz in self.portals_horiz:
            pygame.draw.line(window, self.portal_color, (portal_horiz[0] * UNIT, portal_horiz[1] * UNIT),
                             ((portal_horiz[0] + 1) * UNIT, portal_horiz[1] * UNIT))

        for portal_vertical in self.portals_horiz:
            pygame.draw.line(window, self.portal_color, (portal_vertical[0] * UNIT, portal_vertical[1] * UNIT),
                             (portal_vertical[0] * UNIT, (portal_vertical[1] + 1) * UNIT))

        for wall in self.walls:
            # pygame.draw.rect(window, self.wall_color, (wall[0] * UNIT, wall[1] * UNIT, UNIT, UNIT))
            # pygame.draw.rect(window, WHITE, (wall[0] * UNIT, wall[1] * UNIT, UNIT, UNIT), 1)
            window.blit(self.WALL_IMAGE, (wall[0] * UNIT, wall[1] * UNIT))

    @staticmethod
    def get_random_pos_4_walls(walls, nb_walls):
        """ Returns a set of walls with a maximum of `nb_wall` """
        head_x = WINDOW_WIDTH // 2
        head_y = WINDOW_HEIGHT // 2
        snake_init_pos = {(head_x + i, head_y) for i in range(-2, 3)}
        snake_init_pos.update(walls)
        walls = {get_random_pos_except(snake_init_pos) for _ in range(nb_walls)}

        return set(filter(lambda w: all([is_exitable(n, walls) for n in get_neighbors(w, walls)]), walls))

    @staticmethod
    def get_random_level(nb_walls=20):
        walls = Level.get_random_pos_4_walls(set(), nb_walls=nb_walls)
        return Level(walls=walls, target_score=30)

    @staticmethod
    def create_cage(cage_begin, cage_end):
        # horizontal walls
        walls = {(col, cage_begin[1]) for col in range(cage_begin[0], cage_end[0] + 1)}
        walls.update({(col, cage_end[1]) for col in range(cage_begin[0], cage_end[0] + 1)})
        # vertical walls
        walls.update(
            {(cage_begin[0], row) for row in range(cage_begin[1], cage_end[1] + 1)})
        walls.update(
            {(cage_end[0], row) for row in range(cage_begin[1], cage_end[1] + 1)})
        return walls

    @staticmethod
    def make_doors_on_cage(cage_begin, cage_end):
        walls_to_remove = set()
        horizontal_doors = {(cage_begin[0] + random.randint(1, cage_end[0] - cage_begin[0] - 1), cage_begin[1]),
                            (cage_begin[0] + random.randint(1, cage_end[0] - cage_begin[0] - 1), cage_end[1])}
        vertical_doors = {(cage_begin[0], cage_begin[1] + random.randint(1, cage_end[1] - cage_begin[1] - 1)),
                          (cage_end[0], cage_begin[1] + random.randint(1, cage_end[1] - cage_begin[1] - 1))}
        return horizontal_doors.union(vertical_doors)

