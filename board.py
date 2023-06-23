from random import randrange
from cell import Cell


class Board:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        # Matrix if size dimension x dimension holding Cell object
        self.cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_mines()
        self.get_adjacent()

    def create_mines(self):
        """ Randomly place mines in thr cell matrix """
        mines = []  # Used to keep track of mine positions
        while len(mines) < self.num_mines:
            x, y = randrange(self.rows), randrange(self.cols)
            if (x, y) not in mines:  # Makes sure mine doesn't already exist
                mines.append((x, y))
                self.cells[x][y].mine = True

    def get_adjacent(self):
        """
        Changes Cell's "adjacent_mines" variable to denote the number of surrounding mines.
        If the current cell block is a mine, it will have a -1.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].mine is True:
                    self.cells[row][col].adjacent_mines = -1
                else:
                    self.cells[row][col].adjacent_mines = self.count_mines(row, col)

    def count_mines(self, row, col):
        """ Returns number of mines surrounding a block """
        count = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                # Skip the cell we're currently at
                if x == 0 and y == 0:
                    continue
                row_2 = row + x
                col_2 = col + y
                # Index out of bounds
                if row_2 < 0 or row_2 > self.rows - 1 or col_2 < 0 or col_2 > self.cols - 1:
                    continue
                # Neighboring cell is a mine, increase count
                if self.cells[row_2][col_2].mine:
                    count = count + 1
        return count

    def update_cell(self, row, col, first_click):
        """ Will update cells depending on the clicked cell's attributes """
        cell = self.cells[row][col]
        # Will not update any cells that have been searched or that are flagged
        if cell.searched is True or cell.flag is True:
            return False
        # If the first cell to be clicked is a mine, move it and update adjacent_mines and searched bool
        elif cell.mine is True and first_click is True:
            self.swap_mines(row, col)
            self.search_cell(row, col)
            return False
        # If the cell clicked is a mine (and not first clicked), game is over
        elif cell.mine is True and first_click is False:
            return True
        # A regular cell will get searched
        else:
            self.search_cell(row, col)
            return False

    def search_cell(self, row, col):
        """
        Recursive function that starts from the clicked cell and reveals all neighbors until only the cells
        with 0 adjacent mines (+ 1 more cell from each direction) are shown
        """
        # Only look at new cells, otherwise, this recursive function will go on indefinitely
        if self.cells[row][col].searched is True:
            return

        self.cells[row][col].searched = True
        if self.cells[row][col].adjacent_mines == 0:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == y == 0:
                        continue
                    row_2 = row + x
                    col_2 = col + y
                    if row_2 < 0 or row_2 >= self.rows or col_2 < 0 or col_2 >= self.cols:
                        continue
                    self.search_cell(row_2, col_2)

    def swap_mines(self, row, col):
        """ Swaps mine to a random non-mine cell. Update the adjacent neighbors """
        while True:
            x = randrange(self.rows)
            y = randrange(self.cols)

            if self.cells[x][y].mine is False:
                self.cells[x][y].mine = True
                self.cells[row][col].mine = False
                self.get_adjacent()
                return

    def add_flag(self, row, col):
        self.cells[row][col].flag = True

    def remove_flag(self, row, col):
        self.cells[row][col].flag = False

    def player_won(self):
        count = 0
        for x in range(self.rows):
            for y in range(self.cols):
                if self.cells[x][y].searched is False:
                    count = count + 1
        if count == self.num_mines:
            return True
        else:
            return False

