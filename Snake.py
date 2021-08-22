from Inits import *


class Snake:
    FOOD_IMAGE = pygame.image.load(FILE_PATH + 'image_files/snake_food_2.png')
    APPLE_IMAGE = pygame.image.load(FILE_PATH + 'image_files/apple2.png')
    SNAKE_EAT_FOOD_SOUND = pygame.mixer.Sound(FILE_PATH + 'audio_files/snake_eating.wav')

    def __init__(self, walls):
        head_x = WINDOW_WIDTH // 2
        head_y = WINDOW_HEIGHT // 2
        self.positions = [(head_x, head_y), (head_x - 1, head_y),
                          (head_x - 2, head_y)]
        self.direction = ((self.positions[0][0] - self.positions[1][0]),
                          (self.positions[0][1] - self.positions[1][1]))
        self.is_alive = True

        exceptions = set(self.positions)
        exceptions.update(walls)
        self.food_pos = get_random_pos_except(exceptions)
        self.tail_last_pos = self.positions[-1]  # just temp initialisation. Correctly init. after first move().

    def move(self, direction_to_move):
        assert self.direction[0] != -1 * direction_to_move[0] or \
               self.direction[1] != -1 * direction_to_move[1]

        self.tail_last_pos = self.positions.pop()
        current_head = self.positions[0]
        new_head = (current_head[0] + direction_to_move[0],
                    current_head[1] + direction_to_move[1])
        self.positions.insert(0, new_head)
        self.direction = (self.positions[0][0] - self.positions[1][0],
                          self.positions[0][1] - self.positions[1][1])

    def draw(self, window):
        pos_head = self.positions[0]
        pygame.draw.rect(window, YELLOW,
                         (pos_head[0] * UNIT, pos_head[1] * UNIT, UNIT, UNIT))

        for position in self.positions[1:]:
            pygame.draw.rect(window, GREEN,
                             (position[0] * UNIT, position[1] * UNIT, UNIT, UNIT))
            pygame.draw.rect(window, YELLOW,
                             (position[0] * UNIT, position[1] * UNIT, UNIT, UNIT), 1)

        # food
        window.blit(self.APPLE_IMAGE, (self.food_pos[0] * UNIT, self.food_pos[1] * UNIT))

    def eat_food(self, walls):
        self.SNAKE_EAT_FOOD_SOUND.play()
        self.grow()
        exceptions = set(self.positions)
        exceptions.update(walls)
        self.food_pos = get_random_pos_except(exceptions)

    def grow(self):
        """
            - Grows one chunk into an appropriate position.
            - Doesn't grow if there are no such positions.
        """
        tail_x, tail_y = self.positions[-1]

        possible_positions = (self.tail_last_pos,
                              (tail_x, tail_y - 1),
                              (tail_x, tail_y + 1),
                              (tail_x + 1, tail_y),
                              (tail_x - 1, tail_y))
        grown = False
        for pos in possible_positions:
            if not grown and self.is_appropriate_pos_to_grow_to(pos):
                self.positions.append(pos)
                grown = True

    def is_appropriate_pos_to_grow_to(self, pos):
        return (not pos_out_of_bounds(pos)) and (pos not in self.positions)

    def is_biting_itself(self):
        return self.positions[0] in self.positions[1:]
