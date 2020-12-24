import random
import pygame
from pygame.locals import *
import figures

BLOCK_SIZE = 25
X_GRID_SIZE = 10
Y_GRID_SIZE = 32

WIDTH = X_GRID_SIZE * BLOCK_SIZE
HEIGHT = Y_GRID_SIZE * BLOCK_SIZE


class Game:

    def __init__(self):
        self.isPlaying = True
        self.displayHandle = None
        self.clock = pygame.time.Clock()

        self.field = []

        self.gameBlock = self.get_new_block()

        self.accumulator = 0

    def setup_display(self):
        self.displayHandle = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("pyTetris")

    def setup_field(self):
        for y in range(Y_GRID_SIZE):
            line = []
            for x in range(X_GRID_SIZE):
                line.append(0)
            self.field.append(line)

    def init(self):
        pygame.init()
        self.setup_display()
        self.setup_field()

    def destroy(self):
        pygame.quit()

    def get_new_block(self):
        candidates = [figures.L, figures.L2, figures.S, figures.S2, figures.B, figures.I, figures.T]
        return random.choice(candidates)()

    def block_touches_field(self):
        for line in range(len(self.gameBlock.body)):
            for block in range(len(self.gameBlock.body[line])):
                if self.gameBlock.body[line][block] == 1:
                    if self.field[line + self.gameBlock.y][block + self.gameBlock.x] == 1:
                        return True
        return False

    def handle_keys(self, key):
        if key == pygame.K_SPACE:
            self.gameBlock.rotate()
            # bounds
            if self.gameBlock.x + 3 > X_GRID_SIZE - 1:
                self.gameBlock.x = X_GRID_SIZE - len(self.gameBlock.body[0])
            if self.gameBlock.x < 0:
                self.gameBlock.x = 0

        elif key == pygame.K_LEFT and self.gameBlock.get_left_x() > 0:
            self.gameBlock.x = self.gameBlock.x - 1
            # future (prevent collision)
            if self.block_touches_field():
                self.gameBlock.x = self.gameBlock.x + 1

        elif key == pygame.K_RIGHT and self.gameBlock.get_right_x() < X_GRID_SIZE - 1:
            self.gameBlock.x = self.gameBlock.x + 1
            # future (prevent collision)
            if self.block_touches_field():
                self.gameBlock.x = self.gameBlock.x - 1

        elif key == pygame.K_DOWN:
            self.gameBlock.y = self.gameBlock.y + 1

    def handle_event(self, event):
        if event.type == QUIT:
            self.isPlaying = False
        if event.type == pygame.KEYUP:
            self.handle_keys(event.key)

    def is_empty_line(self, line):
        count = 0
        for i in range(X_GRID_SIZE):
            if self.field[line][i] == 1:
                count = count + 1
        if count == 0:
            return True
        return False

    def check_union(self):
        for line in range(Y_GRID_SIZE):
            count = 0
            for block in range(X_GRID_SIZE):
                if self.field[line][block] == 1:
                    count = count + 1
            if count == X_GRID_SIZE:
                self.field[line] = []
                for _ in range(X_GRID_SIZE):
                    self.field[line].append(0)
        self.concat_field()

    def concat_field(self):
        pops = []
        for line in range(Y_GRID_SIZE):
            if self.is_empty_line(line):
                pops.append(line)
        for line in pops:
            self.field.pop(line)
            self.field.insert(0, [0 for _ in range(X_GRID_SIZE)])

    def add_figure_to_grid(self):
        x = self.gameBlock.x
        y = self.gameBlock.y

        for line in range(len(self.gameBlock.body)):
            for block in range(len(self.gameBlock.body[line])):
                if self.gameBlock.body[line][block] == 1:
                    self.field[y + line - 1][x + block] = 1
        self.check_union()

    def tick(self, _framerate):
        self.accumulator = self.accumulator + 2
        if self.accumulator == 60:
            self.accumulator = 0
            self.gameBlock.y = self.gameBlock.y + 1  # gravity

        if self.gameBlock.get_lowest_y() == Y_GRID_SIZE or self.block_touches_field():
            self.add_figure_to_grid()
            self.gameBlock = self.get_new_block()

    def render_block(self, x, y):
        pygame.draw.rect(self.displayHandle, pygame.color.Color(255, 255, 255), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.displayHandle, pygame.color.Color(100, 100, 255), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def render_field(self):
        for x in range(X_GRID_SIZE):
            for y in range(Y_GRID_SIZE):
                if self.field[y][x] == 1:
                    self.render_block(x, y)

    def render_background(self):
        for line in range(Y_GRID_SIZE):
            for block in range(X_GRID_SIZE):
                pygame.draw.rect(self.displayHandle, pygame.color.Color(100, 100, 255), (block * BLOCK_SIZE, line * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)  # border

    def render(self):

        self.displayHandle.fill(pygame.Color(80, 80, 80))  # clear
        self.render_background()

        self.render_field()

        line_n = 0
        block_n = 0
        for line in self.gameBlock.body:
            for block in line:
                if block == 0:
                    block_n = block_n + 1
                    continue
                x = self.gameBlock.x + block_n
                y = self.gameBlock.y + line_n

                self.render_block(x, y)

                block_n = block_n + 1
            block_n = 0
            line_n = line_n + 1

    def play(self):
        while self.isPlaying:
            tick = self.clock.tick(60)
            self.tick(tick)
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()
            pygame.display.update()
        self.destroy()
