from abc import ABC, abstractmethod
from player import *


class Piece(ABC):
    def __init__(self, player: Player, row: int, col: int, kind: str):
        self.player = player
        self.row = row
        self.col = col
        self.type = kind

    @abstractmethod
    def possible_moves(self, board):
        pass

    def __str__(self):
        return f"{self.type} \ncords: {self.row, self.col} \nplayer: {self.player.color}"


class Pawn(Piece):
    def __init__(self, player, row, col, kind="Pawn"):
        super().__init__(player, row, col, kind)
        self.has_moved = False

    def possible_moves(self, board):
        options = []
        color_direction = 1 if self.player.color == "White" else -1
        if board[self.row - 1 * color_direction][self.col].is_empty():  # check in front of him
            options.append((self.row - 1 * color_direction, self.col))

        if not self.has_moved:
            if board[self.row - 2 * color_direction][self.col].is_empty():  # check 2 blocks in front of him
                options.append((self.row - 2 * color_direction, self.col))

        options += self.capture_moves(board, color_direction)

        return options

    def capture_moves(self, board, color_direction):
        options = []
        if self.col < len(board) - 1:
            if not board[self.row - 1 * color_direction][self.col + 1].is_empty():  # diagonal left option to capture
                if board[self.row - 1 * color_direction][self.col + 1].occupied.player != self.player:
                    options.append((self.row - 1 * color_direction, self.col + 1))

        if self.col != 0:
            if not board[self.row - 1 * color_direction][self.col - 1].is_empty():  # diagonal right option to capture
                if board[self.row - 1 * color_direction][self.col - 1].occupied.player != self.player:
                    options.append((self.row - 1 * color_direction, self.col - 1))

        return options


class Rook(Piece):
    def __init__(self, player, row, col, kind="Rook"):
        super().__init__(player, row, col, kind)

    def possible_moves(self, board):
        options = []
        directions = [1, -1]

        for direction in directions:  # checks left and right, and then up and down
            i = 1
            while True:
                col = self.col + i * direction
                if not (0 <= col < len(board[0])):
                    break  # Break the loop if col is out of bounds

                if board[self.row][col].is_empty():
                    options.append((self.row, col))
                else:  # piece in the way
                    if board[self.row][col].occupied.player != self.player:
                        options.append((self.row, col))
                    break

                i += 1

        for direction in directions:  # checks up and down
            i = 1
            while True:
                row = self.row + i * direction
                if not (0 <= row < len(board[0])):
                    break  # Break the loop if col is out of bounds

                if board[row][self.col].is_empty():
                    options.append((row, self.col))
                else:  # piece in the way
                    if board[row][self.col].occupied.player != self.player:
                        options.append((row, self.col))
                    break

                i += 1

        return options


class Bishop(Piece):
    def __init__(self, player, row, col, kind="Bishop"):
        super().__init__(player, row, col, kind)

    def possible_moves(self, board):
        options = []

        directions_x = [1, -1]
        directions_y = [1, -1]
        for direction_y in directions_y:  # checks diagonals
            for direction_x in directions_x:
                i = 1
                while True:
                    row = self.row + i * direction_x
                    col = self.col + i * direction_y
                    if not (0 <= col < len(board) and 0 <= row < len(board)):
                        break  # Break the loop if row and col is out of bounds

                    if board[row][col].is_empty():
                        options.append((row, col))
                    else:  # piece in the way
                        if board[row][col].occupied.player != self.player:
                            options.append((row, col))
                        break

                    i += 1
        return options


class Knight(Piece):
    def __init__(self, player, row, col, kind="Knight"):
        super().__init__(player, row, col, kind)

    def possible_moves(self, board):
        options = []

        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:  # Knight moves in an L-shape
                    new_row, new_col = self.row + i, self.col + j

                    if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                        square = board[new_row][new_col]

                        if square.is_empty():
                            options.append((new_row, new_col))
                        elif square.occupied.player != self.player:
                            options.append((new_row, new_col))

        return options


class Queen(Bishop, Rook):
    def __init__(self, player, row, col):
        Bishop.__init__(self, player, row, col, "Queen")

    def possible_moves(self, board):
        bishop_moves = Bishop.possible_moves(self, board)
        rook_moves = Rook.possible_moves(self, board)

        return bishop_moves + rook_moves


class King(Piece):
    def __init__(self, player, row, col, kind="King"):
        super().__init__(player, row, col, kind)
        self.in_check = False

    def possible_moves(self, board):
        options = []

        for j in range(-1, 2, 1):
            for i in range(-1, 2, 1):
                if i == 0 and j == 0:  # the cords of the piece itself
                    continue
                if 0 <= self.row + j < len(board) and 0 <= self.col + i < len(board):  # if in boundaries of board
                    square = board[self.row + j][self.col + i]
                    if square.is_empty() or square.occupied.player != self.player:
                        options.append((self.row + j, self.col + i))
        return options
