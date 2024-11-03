import math


ESC = "\033"
RESET = f"{ESC}[0m"
BOLD = f"{ESC}[1m"


def FOREGROUND(x):
    return f"{ESC}[38;5;{x}m"


def BACKGROUND(x):
    return f"{ESC}[48;5;{x}m"


def BLACK(x):
    return f"{FOREGROUND(0)}{x}{RESET}"


def RED(x):
    return f"{FOREGROUND(196)}{x}{RESET}"


def BLUE(x):
    return f"{FOREGROUND(21)}{x}{RESET}"


def GREEN(x):
    return f"{FOREGROUND(76)}{x}{RESET}"


def COLOR(color, x):
    return f"{FOREGROUND(color)}{x}{RESET}"


def FB_COLOR(fore, back, x):
    return f"{FOREGROUND(fore)}{BACKGROUND(back)}{x}{RESET}"


SQUARE = "██"
HALF_SQUARE = "█"
BLACK_SQUARE = f"{FOREGROUND(0)}{SQUARE}{RESET}"
RED_SQUARE = f"{FOREGROUND(196)}{SQUARE}{RESET}"
BLUE_SQUARE = f"{FOREGROUND(21)}{SQUARE}{RESET}"
GREEN_SQUARE = f"{FOREGROUND(76)}{SQUARE}{RESET}"


class Screen:
    def __init__(self, values) -> None:
        self.values = [list(row) for row in values]

    @property
    def width(self):
        return len(self.values[0])

    @property
    def height(self):
        return len(self.values)

    def print(self):
        for row in self.values:
            for char in row:
                print(char, end="")
            print()

    def set_char(self, x, y, value):
        if x >= 0 and y >= 0 and y < len(self.values) and x < len(self.values[y]):
            self.values[y][x] = value


def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


SCREEN_WIDTH = 60
SCREEN_HEIGHT = 60


class Canvas:
    def __init__(self, width, height) -> None:
        self.screen = Screen([[SQUARE]*SCREEN_WIDTH]*SCREEN_HEIGHT)
        self.width = width
        self.height = height

    def draw_rect(self, x, y, width, height, char):
        screen = self.screen
        sim_width = self.width
        sim_height = self.height

        x_scaling_factor = screen.width/sim_width
        y_scaling_factor = screen.height/sim_height
        screen_x_start = round(x*x_scaling_factor)
        screen_x_end = round((x+width)*x_scaling_factor)
        screen_y_start = round(y*y_scaling_factor)
        screen_y_end = round((y+height)*y_scaling_factor)
        for i in range(screen_x_start, screen_x_end):
            for j in range(screen_y_start, screen_y_end):
                screen.set_char(i, j, char)

    def draw_circle(self, x, y, radius, char):
        screen = self.screen
        sim_width = self.width
        sim_height = self.height

        x_scaling_factor = screen.width/sim_width
        y_scaling_factor = screen.height/sim_height
        screen_x_start = round((x-radius)*x_scaling_factor)
        screen_x_end = round((x+radius)*x_scaling_factor)
        screen_y_start = round((y-radius)*y_scaling_factor)
        screen_y_end = round((y+radius)*y_scaling_factor)
        # print(screen_x_start,screen_x_end,screen_y_start,screen_y_end)
        for i in range(screen_x_start, screen_x_end):
            for j in range(screen_y_start, screen_y_end):
                if dist((i+0.5)/x_scaling_factor, (j+0.5)/y_scaling_factor, x, y) <= radius:
                    screen.set_char(i, j, char)

    def display(self):
        self.screen.print()

    def clear(self):
        self.screen = Screen([[SQUARE]*SCREEN_WIDTH]*SCREEN_HEIGHT)


class Text_Canvas:
    def __init__(self, width, height) -> None:
        self.screen = Screen([[HALF_SQUARE]*width]*height)
        self.width = width
        self.height = height

    def draw_text(self, x, y, text, fcolor, bcolor):
        for i, char in enumerate(text):
            self.screen.set_char(x+i, y, FB_COLOR(fcolor, bcolor, char))

    def draw_rect(self, x, y, w, h, color):
        for i in range(w):
            for j in range(h):
                self.screen.set_char(x+i, y+j, COLOR(color, HALF_SQUARE))

    def display(self):
        self.screen.print()

    def clear(self):
        self.screen = Screen([[HALF_SQUARE]*self.width]*self.height)
