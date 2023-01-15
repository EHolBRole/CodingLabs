import pathlib
import random as r
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    matrix = list()
    counter = 0
    row: tp.List[T]
    row = list()
    n = n
    for el in values:
        if counter == n:
            matrix.append(row)
            row = list()
            counter = 0
        row.append(el)
        counter += 1
    matrix.append(row)
    return matrix


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]):
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = list()
    for row in grid:
        col.append(row[pos[1]])
    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = list()

    block_pos = [(pos[0] + 1), (pos[1] + 1)]
    while block_pos[0] % 3 != 0:
        block_pos[0] += 1
    while block_pos[1] % 3 != 0:
        block_pos[1] += 1

    for r in range(block_pos[0] - 3, block_pos[0]):
        for c in range(block_pos[1] - 3, block_pos[1]):
            block.append(grid[r][c])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Tuple[int, int]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for r in range(0, len(grid)):
        for c in range(0, len(grid[r])):
            if grid[r][c] == ".":
                return r, c
    a = 2
    return int(-1), int(-1)


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

    values_to_remove = set()

    row = get_row(grid, pos)

    for el in row:
        for val in values:
            if el == val:
                values_to_remove.add(el)
    for val in values_to_remove:
        values.remove(val)

    values_to_remove = set()

    col = get_col(grid, pos)

    for el in col:
        for val in values:
            if el == val:
                values_to_remove.add(el)
    for val in values_to_remove:
        values.remove(val)

    values_to_remove = set()

    block = get_block(grid, pos)

    for el in block:
        for val in values:
            if el == val:
                values_to_remove.add(el)
    for val in values_to_remove:
        values.remove(val)
    return values


def solve(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    a = int(-1), int(-1)
    if pos != a:
        posval = find_possible_values(grid, pos)
        for val in posval:
            grid[pos[0]][pos[1]] = val
            grid = solve(grid)
            pos2 = find_empty_positions(grid)
            if pos2 == a:
                return grid
        ala = find_empty_positions(grid)
        a = int(-1), int(-1)
        if ala != a:
            grid[pos[0]][pos[1]] = "."
        return grid
    else:
        return grid


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles

    for i in range(0, 9):
        row = get_row(solution, (i, i))
        values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        col = get_col(solution, (i, i))
        for r in row:
            inValues = False
            for v in values:
                if r == v:
                    inValues = True
                    values.remove(v)
                    break
            if not inValues:
                return False

        values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

        for c in col:
            inValues = False
            for v in values:
                if c == v:
                    inValues = True
                    values.remove(v)
                    break
            if not inValues:
                return False

        if (i + 1) % 3 == 0:
            block = get_block(solution, (i, i))

            values = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

            for b in block:
                inValues = False
                for v in values:
                    if b == v:
                        inValues = True
                        values.remove(v)
                        break
                if not inValues:
                    return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    empty = [["." for i in range(9)] for j in range(9)]
    grid = solve(empty)
    if grid is not None:
        k_empty = 81 - min(81, N)

        while k_empty != 0:
            row = r.randint(0, 8)
            col = r.randint(0, 8)
            if grid[row][col] != ".":
                grid[row][col] = "."
                k_empty -= 1
        return grid
    else:
        return []
    pass


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
