import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.rows * cell_size
        self.height = life.cols * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        # Copy from previous assignment
        x = 1
        y = 1
        for raw in self.life.curr_generation:
            for el in raw:
                if el == 0:
                    pygame.draw.rect(
                        self.screen,
                         pygame.Color("white"),
                         (x, y, self.cell_size - 1, self.cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (x, y, self.cell_size - 1, self.cell_size - 1),
                    )
                x += self.cell_size
            y += self.cell_size
            x = 1
        pass

    def edit_cell(self, x, y) -> None:
        row = y // self.cell_size
        col = x // self.cell_size
        if self.life.curr_generation[row][col] == 0:
            self.life.curr_generation[row][col] = 1
        else:
            self.life.curr_generation[row][col] = 0

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.edit_cell(x, y)
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
            if self.life.is_max_generations_exceeded:
                running = False
            elif not self.life.is_changing:
                running = False
            if not pause:
                self.life.step()
                self.draw_lines()
                self.draw_grid()
                pygame.display.flip()

            clock.tick(self.speed)
        pygame.quit()
        pass


game = GameOfLife(size=(25, 25), randomize=True)
gui = GUI(life=game, cell_size=20, speed=5)
gui.run()
