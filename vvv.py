import random
import os
import time
import sys
import tty
import termios

# Определяем размеры поля
WIDTH = 10
HEIGHT = 20

# Определяем фигуры
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

class Tetris:
    def __init__(self):
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_shape = self.new_shape()
        self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

    def new_shape(self):
        return random.choice(SHAPES)

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def can_move(self, dx, dy):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + x + dx
                    new_y = self.current_y + y + dy
                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT or self.board[new_y][new_x]:
                        return False
        return True

    def merge_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + y][self.current_x + x] = 1

    def clear_lines(self):
        self.board = [row for row in self.board if any(cell == 0 for cell in row)]
        while len(self.board) < HEIGHT:
            self.board.insert(0, [0] * WIDTH)

    def draw_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.board:
            print(' '.join(['#' if cell else '.' for cell in row]))
        print(f"Current shape position: ({self.current_x}, {self.current_y})")

    def get_char(self):
        """Получить символ из стандартного ввода без ожидания нажатия Enter."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        while True:
            self.draw_board()
            if self.can_move(0, 1):
                self.current_y += 1
            else:
                self.merge_shape()
                self.clear_lines()
                self.current_shape = self.new_shape()
                self.current_x = WIDTH // 2 - len(self.current_shape[0]) // 2
                self.current_y = 0
                if not self.can_move(0, 0):
                    print("Game Over!")
                    break
            
            # Обработка ввода
            if self.get_char() == 'a':  # Влево
                if self.can_move(-1, 0):
                    self.current_x -= 1
            elif self.get_char() == 'd':  # Вправо
                if self.can_move(1, 0):
                    self.current_x += 1
            elif self.get_char() == 's':  # Ускорение вниз
                if self.can_move(0, 1):
                    self.current_y += 1
            elif self.get_char() == 'q':  # Выход
                print("Выход из игры.")
                break

            time.sleep(0.5)

if __name__ == "__main__":
    game = Tetris()
    game.run()
