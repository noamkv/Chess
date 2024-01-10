from square import *
from pieces import *
from player import *


def create_empty_board(size=8):
    return [[Square() for _ in range(size)] for _ in range(size)]


def create_board(player1, player2):
    board = create_empty_board()
    place_pawns(board, player1, player2)
    place_rooks(board, player1, player2)
    place_bishops(board, player1, player2)
    place_knights(board, player1, player2)
    place_queens(board, player1, player2)
    place_kings(board, player1, player2)
    return board


def place_pawns(board, player1: Player, player2: Player):
    for i in range(len(board)):
        board[6][i].occupied = Pawn(player1, 6, i)
    for i in range(len(board)):
        board[1][i].occupied = Pawn(player2, 1, i)


def place_rooks(board, player1, player2):
    board[7][0].occupied = Rook(player1, 7, 0)  # white rooks
    board[7][7].occupied = Rook(player1, 7, 7)

    board[0][0].occupied = Rook(player2, 0, 0)  # black rooks
    board[0][7].occupied = Rook(player2, 0, 7)


def place_bishops(board, player1, player2):
    board[7][2].occupied = Bishop(player1, 7, 2)
    board[7][5].occupied = Bishop(player1, 7, 5)

    board[0][2].occupied = Bishop(player2, 0, 2)
    board[0][5].occupied = Bishop(player2, 0, 5)


def place_knights(board, player1, player2):
    board[7][1].occupied = Knight(player1, 7, 1)
    board[7][6].occupied = Knight(player1, 7, 6)

    board[0][1].occupied = Knight(player2, 0, 1)
    board[0][6].occupied = Knight(player2, 0, 6)


def place_queens(board, player1, player2):
    board[7][3].occupied = Queen(player1, 7, 3)
    board[0][3].occupied = Queen(player2, 0, 3)


def place_kings(board, player1, player2):
    board[7][4].occupied = King(player1, 7, 4)
    board[0][4].occupied = King(player2, 0, 4)
