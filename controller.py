import pygame
from minesweeper import Minesweeper, GameState
from drop_down import DropDown

# GLOBALS
FPS = 60
MENU_HEIGHT = 30
CELL_MARGIN = 1

MINE_SOUND = None
SEARCH_SOUND = None

LEVELS = {
    "Easy": {
        "cells": (9, 9),
        "cell_size": 25,
        "mines": 10,
    },
    "Medium": {
        "cells": (15, 15),
        "cell_size": 25,
        "mines": 40,
    },
    "Hard": {
        "cells": (16, 30),
        "cell_size": 25,
        "mines": 99,
    }
}


def set_width_height(cells, cell_size):
    return (cells[1] * cell_size) + (cells[1] - 1) * CELL_MARGIN, \
           (cells[0] * cell_size) + (cells[0] - 1) * CELL_MARGIN + MENU_HEIGHT


class Controller:
    def __init__(self, cells, cell_size, mines):
        pygame.init()
        pygame.display.set_caption("Minesweeper")

        self.clock = pygame.time.Clock()

        self.width, self.height = set_width_height(cells, cell_size)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.minesweeper = Minesweeper(cells, cell_size, mines)
        self.menu = DropDown(self.width, MENU_HEIGHT)

        self.is_running = True
        self.game_state = GameState.PLAYING

    def running(self):
        while self.is_running:
            self.events()
            self.draw()
            if self.menu.is_open:
                self.menu.update_hover()
            self.clock.tick(FPS)
        pygame.quit()

    def draw(self):
        self.screen.blit(self.minesweeper.draw_board(), (0, MENU_HEIGHT))
        self.screen.blit(self.menu.draw(), (0, 0))
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_clicked()
                elif event.button == 3:
                    self.right_clicked()

    def left_clicked(self):
        """ User left-clicked on anywhere in the program """
        pos = pygame.mouse.get_pos()
        # User clicked on the top bar menu
        if 0 <= pos[0] <= self.width and 0 <= pos[1] <= MENU_HEIGHT:
            self.menu.menu_clicked(pos)
        # The menu is open
        elif self.menu.is_open:
            level = self.menu.opt_clicked(pos)
            # User clicked on an option, so the board will create a new game
            if level is not None:
                self.minesweeper = Minesweeper(LEVELS[level]["cells"],
                                               LEVELS[level]["cell_size"], LEVELS[level]["mines"])
                self.width, self.height = set_width_height(LEVELS[level]["cells"], LEVELS[level]["cell_size"])
                self.screen = pygame.display.set_mode((self.width, self.height))
                self.menu.update_width(self.width)
                self.menu.update_message("", "won")
                self.game_state = GameState.PLAYING
        # Game is ongoing and user left-clicked on a cell in the grid
        elif self.menu.is_open is False and self.game_state == GameState.PLAYING:
            pos = pygame.mouse.get_pos()
            state = self.minesweeper.clicked(pos)
            if state == GameState.LOST:
                self.game_state = GameState.LOST
                self.menu.update_message("You Lost", "lost")
            elif state == GameState.WON:
                self.game_state = GameState.WON
                self.menu.update_message("You Won", "won")

    def right_clicked(self):
        """ User right-clicked on a cell in the grid """
        pos = pygame.mouse.get_pos()
        if 0 <= pos[0] <= self.width and pos[1] >= MENU_HEIGHT and self.game_state == GameState.PLAYING:
            self.minesweeper.cell_flagged(pos)


if __name__ == '__main__':
    controller = Controller(LEVELS["Easy"]["cells"], LEVELS["Easy"]["cell_size"], LEVELS["Easy"]["mines"])
    controller.running()
