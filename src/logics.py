from pieces import Piece, Pawn, Rook, Bishop, King, Queen


def cords_to_square(square_size, x, y):
    return y // square_size, x // square_size  # the order is replaced because
    # when using the board array the row is first and then the column


def change_turn(players):
    for player in players:
        player.switch_turn()


def get_other_item(lst, item):
    if len(lst) == 2:
        index_of_item = lst.index(item)
        return lst[1 - index_of_item]
    else:
        return None


def board_to_window(piece, square_size):
    x = piece.col * square_size
    y = piece.row * square_size
    return x, y


def move_piece(board, piece: Piece, row, col):
    board[row][col].occupied = piece
    board[piece.row][piece.col].occupied = None
    piece.row = row
    piece.col = col
    if isinstance(piece, Pawn):
        piece.has_moved = True
        if row == 0 or row == len(board) - 1:
            board[row][col].occupied = Queen(piece.player, row, col)


def find_king(board, player):
    for i in range(len(board)):
        for j in range(len(board)):
            square = board[i][j]
            if not square.is_empty():
                if type(square.occupied) is King:
                    if square.occupied.player.color == player.color:
                        return square.occupied
    return None


def all_possible_moves(board, player):
    moves = []
    for i in range(len(board)):
        for j in range(len(board)):
            square = board[i][j]
            if not square.is_empty():
                if player is not square.occupied.player:
                    moves += square.occupied.possible_moves(board)
    return moves


def is_king_in_check(board, king):
    threats = all_possible_moves(board, king.player)
    if (king.row, king.col) in threats:
        print("check")
        return True
    return False


def move_is_valid(board, piece, row, col) -> bool:
    """ function plays the move see if it is valid -> not creating check on yourself .
        the function goes back and returns if it is valid """

    is_valid = None
    save_piece = None
    save_cords = (piece.row, piece.col)

    if not board[row][col].is_empty():
        save_piece = piece

    move_piece(board, piece, row, col)

    king = find_king(board, piece.player)
    if king is not None:
        if is_king_in_check(board, king):
            is_valid = False
        else:
            is_valid = True
    else:
        is_valid = True

    # reset the board
    move_piece(board, piece, save_cords[0], save_cords[1])

    board[row][col].occupied = save_piece

    return is_valid


def check_for_checks(board, players):
    for player in players:
        king = find_king(board, player)
        if is_king_in_check(board, king):
            king.in_check = True
            king.in_check = True
        else:
            king.in_check = False


def check_checkmate_or_stalemate(board, players):
    # TODO
    pass