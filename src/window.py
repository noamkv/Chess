import pygame
import sys
from set_up_board import *
from logics import *


class Window:
    def __init__(self, size, color="Green", board_array=None, players=None):
        pygame.init()
        self.board_size = 8
        self.color = color
        self.width = size
        self.height = size
        self.board_array = board_array
        self.square_size = self.width // self.board_size

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Noam's chess game")
        self.board_path = f"../images/Boards/{self.color}Board.png"
        self.board = pygame.image.load(self.board_path).convert()
        self.board = pygame.transform.scale(self.board, (self.width, self.height))  # fixes the resolution
        self.window.blit(self.board, (0, 0))

        dot_path = f"../images/dot.png"
        self.dot = pygame.image.load(dot_path).convert()
        self.dot = pygame.transform.scale(self.dot, (self.square_size, self.height))

        self.players = players
        self.selected_piece = None

        self.game_over = False

    def run(self):
        while True:
            self.update_images(self.board_array)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left button
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        row, col = cords_to_square(self.square_size, mouse_x, mouse_y)
                        self.handle_press(row, col)

    def update_images(self, board_array):
        self.window.blit(self.board, (0, 0))  # reprints the screen

        for i in range(len(board_array)):
            for j in range(len(board_array)):
                square = board_array[i][j]
                if not square.is_empty():
                    path = f"../images/Pieces/{square.occupied.player.color}/{square.occupied.player.color}{square.occupied.type}.png"
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (self.square_size, self.square_size))

                    x, y = board_to_window(square.occupied, self.square_size)
                    self.window.blit(image, (x, y))

    def handle_press(self, row, col):
        square = self.board_array[row][col]

        if self.selected_piece is None:
            if not square.is_empty() and square.occupied.player.is_turn:  # selects a piece
                self.selected_piece = square.occupied

        else:
            if square.occupied is not None and square.occupied.player == self.selected_piece.player:  # switch piece
                self.selected_piece = square.occupied

            elif self.selected_piece is not None:
                if (row, col) in self.selected_piece.possible_moves(self.board_array):  # move the piece
                    if move_is_valid(self.board_array, self.selected_piece, row, col):
                        move_piece(self.board_array, self.selected_piece, row, col)
                        self.selected_piece = None

                        check_for_checks(self.board_array, self.players)
                        change_turn(self.players)


def main():
    try:
        white = Player("noam", "White", True)
        black = Player("aviv", "Black", False)
        players = [white, black]
        board = create_board(white, black)
        window = Window(800, "Green", board, players)
        window.run()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()

