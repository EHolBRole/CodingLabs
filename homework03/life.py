import pathlib
import random
import typing as tp
from typing import List

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> grid:
        grid = [[0 for _ in range(0, self.cols)] for _ in range(0, self.rows)]
        if randomize:
            for raw in range(0, len(grid)):
                for el in range(0, len(grid[raw])):
                    grid[raw][el] = random.randint(0, 1)
        return grid
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = list()
        for row in range(-1, 2):
            if cell[0] + row < 0 or cell[0] + row >= self.rows:
                continue
            for col in range(-1, 2):
                if cell[1] + col < 0 or cell[1] + col >= self.cols or row == 0 and col == 0:
                    continue
                neighbours.append(self.curr_generation[row + cell[0]][col + cell[1]])
        return neighbours

    def get_next_generation(self) -> grid:
        # Copy from previous assignment
        next_generation = []
        for row in range(0, self.rows):
            row_list = []
            for col in range(0, self.cols):
                neighbours = self.get_neighbours((row, col))
                if (
                        sum(neighbours) == 3
                        or (sum(neighbours) == 2 and self.curr_generation[row][col] == 1)
                ):
                    row_list.append(1)
                else:
                    row_list.append(0)
            next_generation.append(row_list)
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations == self.max_generations:
            return True
        else:
            return False
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename).readlines()
        input_grid = []
        for ind in range(len(file)):
            row = list(map(int, file[ind].split()))
            input_grid.append(row)
        life = GameOfLife((len(input_grid), len(input_grid[0])), False)
        life.curr_generation = input_grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        for raw in self.curr_generation:
            file.write("".join([str(el) for el in raw]) + "\n")
        pass
