import pygame
from enum import Enum
from board import Board

# GLOBALS
CELL_MARGIN = 1
MENU_HEIGHT = 30

UNSEARCHED_IMG = pygame.image.load("Assets//unsearched.png")
SEARCHED_IMG = pygame.image.load("Assets//searched.png")
FLAGGED_IMG = pygame.image.load("Assets//flag.png")
MINE_IMG = pygame.image.load("Assets//mine.png")

COLORS = {
    1: (225, 0, 0),  # RED
    2: (255, 105, 0),  # ORANGE
    3: (255, 225, 0),  # GOLD
    4: (0, 100, 0),  # GREEN
    5: (0, 255, 255),  # CYAN
    6: (0, 0, 255),  # BLUE
    7: (255, 0, 255),  # MAGENTA
    8: (75, 0, 130),  # INDIGO
    9: (80, 80, 80)  # DARK GRAY
}


class GameState(Enum):
    WON = 1
    LOST = 2
    PLAYING = 3


class Minesweeper:
    def __init__(self, cells, cell_size, mines):
        self.font = pygame.font.SysFont("arial", 20)

        self.rows, self.cols = cells[0], cells[1]
        self.cell_size = cell_size
        self.width = (self.cols * self.cell_size) + CELL_MARGIN * (self.cols - 1)
        self.height = (self.rows * self.cell_size) + CELL_MARGIN * (self.rows - 1)

        self.board = Board(self.rows, self.cols, mines)

        self.game_over = False
        self.first_click = True

    def draw_board(self):
        """ Draws the minesweeper grid with the correct cells throughout the game """

        row_dimension = self.rows * self.cell_size + CELL_MARGIN * self.rows
        col_dimension = self.cols * self.cell_size + CELL_MARGIN * self.cols
        field = pygame.Surface((col_dimension, row_dimension))
        field.fill(COLORS[9])

        # Scales images to be the size of the cells
        searched = pygame.transform.scale(SEARCHED_IMG, (self.cell_size, self.cell_size))
        unsearched = pygame.transform.scale(UNSEARCHED_IMG, (self.cell_size, self.cell_size))
        flagged = pygame.transform.scale(FLAGGED_IMG, (self.cell_size, self.cell_size))
        mine = pygame.transform.scale(MINE_IMG, (self.cell_size, self.cell_size))

        # Draws grid with the correct image based on the status of the cell
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.cell_size * col + (CELL_MARGIN * col)
                y = self.cell_size * row + (CELL_MARGIN * row)

                cell = self.board.cells[row][col]

                # Searched cell: user has searched this cell and does not contain a mine
                if cell.searched is True:
                    field.blit(searched, (x, y))
                    # If the cell has neighboring cell with mines, it will display a number
                    if cell.adjacent_mines > 0:
                        n = cell.adjacent_mines
                        text = self.font.render(str(n), True, COLORS[n])
                        field.blit(text, (x + self.cell_size // 3, y + self.cell_size // 10))
                # Flagged cell: user "flagged" the cell thinking it's a mine
                elif cell.flag is True:
                    field.blit(flagged, (x, y))
                # Unsearched cel : cell hasn't been explored
                elif cell.mine is False and cell.flag is False:
                    field.blit(unsearched, (x, y))
                # Mine: cell with a mine
                # If the user has clicked on a mine, all mines are shown. The cell is shown
                # with a "Flagged" image if flagged, and "Searched" image otherwise
                elif cell.mine is True and self.game_over is True:
                    field.blit(mine, (x, y))
                elif cell.searched is False:
                    field.blit(unsearched, (x, y))
        return field

    def clicked(self, pos):
        """
        When the user left-clicks a cell, a function will be called to either clear cells or
        to tell the program a mine has been hit and the game is over
        """
        row, col = self.get_cell(pos)
        if self.board.update_cell(row, col, self.first_click):
            self.game_over = True
            return GameState.LOST
        if self.board.player_won():
            return GameState.WON
        if self.first_click:
            self.first_click = False
        return GameState.PLAYING

    def cell_flagged(self, pos):
        """
        When the user right-clicks a cell, a cell with a flag will have it removed
        and will add a flag to active or mine cells
        """
        row, col = self.get_cell(pos)
        cell = self.board.cells[row][col]

        if cell.flag is True:
            self.board.remove_flag(row, col)
        elif cell.flag is False and cell.searched is False:
            self.board.add_flag(row, col)

    def get_cell(self, pos):
        """
        Returns the cell row, column that was clicked based on where the mouse position is
        """
        row = col = 0
        y, x = pos[0], pos[1]
        size = self.cell_size + CELL_MARGIN
        while y - size > 0:
            y = y - size
            col = col + 1

        while x - size > MENU_HEIGHT:
            x = x - size
            row = row + 1

        return row, col
