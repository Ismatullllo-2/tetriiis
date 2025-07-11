import random
import os
import time
import sys
import tty
import termios

# Настройки
WIDTH = 10
HEIGHT = 20
EMPTY = '.'
FILLED = '#'

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

class Tetris:
    def __init__(self):
        self.board = [[EMPTY] * WIDTH for _ in range(HEIGHT)]
        self.current_piece = self.new_piece()
        self.current_x = WIDTH // 2 - 1
        self.current_y = 0

    def new_piece(self):
        return random.choice(SHAPES)

    def rotate_piece(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]

    def valid_position(self, dx=0, dy=0):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + x + dx
                    new_y = self.current_y + y + dy
                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT or (new_y >= 0 and self.board[new_y][new_x] == FILLED):
                        return False
        return True

    def merge_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + y][self.current_x + x] = FILLED

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == EMPTY for cell in row)]
        lines_cleared = HEIGHT - len(new_board)
        new_board = [[EMPTY] * WIDTH for _ in range(lines_cleared)] + new_board
        self.board = new_board

    def drop_piece(self):
        if self.valid_position(dy=1):
            self.current_y += 1
        else:
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.new_piece()
            self.current_x = WIDTH // 2 - 1
            self.current_y = 0
            if not self.valid_position():
                return False
        return True

    def display(self):
        os.system('clear')  # Очистка экрана
        # Создаем временное поле для отображения текущей фигуры
        temp_board = [row[:] for row in self.board]
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    temp_y = self.current_y + y
                    temp_x = self.current_x + x
                    if temp_y >= 0:  # Не отображаем фигуру, если она выше игрового поля
                        temp_board[temp_y][temp_x] = FILLED
        for row in temp_board:
            print(' '.join(row))
        print(f"Current piece position: ({self.current_x}, {self.current_y})")

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def get_input(self):
        key = self.getch()
        if self.valid_position(dx=-1) and key == 'a':  # Влево
            self.current_x -= 1
        elif self.valid_position(dx=1) and key == 'd':  # Вправо
            self.current_x += 1
        elif key == 's':  # Вниз
            self.drop_piece()
        elif key == 'w':  # Поворот
            self.rotate_piece()

def main():
    game = Tetris()
    while True:
        game.display()
        game.get_input() 
