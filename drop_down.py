import pygame

# GLOBALS
COLORS = {
    "bar": (180, 180, 180),
    "button": (205, 205, 205),
    "hover": (0, 128, 255),
    "won": (0, 150, 0),
    "lost": (150, 0, 0)
}


class DropDown:
    def __init__(self, width, height):
        self.font = pygame.font.SysFont("arial", 14)
        self.width = width
        self.height = height

        self.main_option = "New Game"
        self.items = ["Easy", "Medium", "Hard"]
        self.hovered_item = -1

        self.button_height = height-4
        self.button_width = 70
        self.opt_width = 60

        self.bar_rect = pygame.Rect(0, 0, self.width, self.height)
        self.button_rect = pygame.Rect(3, 3, self.button_width, self.button_height)
        self.option_rects = []

        for i in range(len(self.items)):
            y_pos = (i * self.button_height) + self.height
            self.option_rects.append(pygame.Rect(0, y_pos, self.opt_width, self.button_height))

        self.is_open = False
        self.message = ""
        self.message_color = COLORS["won"]

    def update_hover(self):
        """ Changes the background color of the menu option that's being hovered over """
        for i, opt in enumerate(self.option_rects):
            if opt.collidepoint(pygame.mouse.get_pos()):
                self.hovered_item = i
                return
        self.hovered_item = -1

    def draw(self):
        """ Draws top bar and button. If the menu is open, draws all options """
        screen = pygame.Surface((self.width, self.height + (self.button_height * 3)), pygame.SRCALPHA, 32)

        pygame.draw.rect(screen, COLORS["bar"], self.bar_rect, 0)
        pygame.draw.rect(screen, COLORS["button"], self.button_rect, 2)
        opt_text = self.font.render(self.main_option, True, (0, 0, 0))
        screen.blit(opt_text, opt_text.get_rect(center=self.button_rect.center))

        if self.is_open:
            for i, text in enumerate(self.items):
                if self.hovered_item == i:
                    pygame.draw.rect(screen, COLORS["hover"], self.option_rects[i], 0)
                else:
                    pygame.draw.rect(screen, COLORS["bar"], self.option_rects[i], 0)
                t = self.font.render(self.items[i], True, (0, 0, 0))
                screen.blit(t, t.get_rect(center=self.option_rects[i].center))

        m = self.font.render(self.message, True, self.message_color)
        screen.blit(m, m.get_rect(center=self.bar_rect.center))

        return screen

    def menu_clicked(self, pos):
        """ Change 'is_open' bool depending status and area clicked """
        if self.button_rect.collidepoint(pos):
            self.is_open = not self.is_open
            return
        elif self.bar_rect.collidepoint(pos):
            self.is_open = False

    def opt_clicked(self, pos):
        """ Will return whichever menu option was clicked"""
        self.is_open = False
        for i, opt in enumerate(self.option_rects):
            if opt.collidepoint(pos):
                return self.items[i]

    def update_width(self, w):
        """ Changes width of menu bar when the user switches between levels """
        self.width = w
        self.bar_rect.width = self.width

    def update_message(self, message, color):
        """ Will display if the player has won or lost a game """
        self.message = message
        self.message_color = COLORS[color]
