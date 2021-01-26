import string
import chess_functions
from string import ascii_uppercase

"""Chessboard is a grid of 1-64."""

pieces = "♔♕♗♘♖♙♚♛♝♞♜♟"


def piece_name_input_flask(app_piece):
    # Get valid chess piece from user from chess-input-1.html
    valid = 0
    message = "Error in chessboard.piece_name_input_flask"
    piece = app_piece
    valid_pieces = ['B', 'Bishop', 'C', 'Castle', 'H', 'Horse', 'KI', 'King', 'KN', 'Knight', 'N', 'Knight', 'P', 'Pawn',
                    'Q', 'Queen', 'R', 'Rook']
    if not piece.isalpha():
        message = "Piece names only use letters."
        piece = 0
        return message, piece, valid
    elif piece.upper() == 'K':
        message = "\"K\" what? Be more specific."
        piece = 0
        return message, piece, valid
    elif (piece.upper()[0] not in valid_pieces) and (piece.upper()[:2] not in valid_pieces):
        message = "The chess pieces are: King, Queen, Bishop, Knight, Rook, and Pawn."
        piece = 0
        return message, piece, valid
    elif piece.isalpha() and ((piece.upper()[0] in valid_pieces) or (piece.upper()[:2]) in valid_pieces):
        p: str = piece.upper()

        # special cases:
        if p[0] == "H":
            message = "Your piece is a Knight, NOT a Horse:"
            piece = "N"
        elif p[0] == "C":
            message = "Your piece is a Rook, a.k.a. a Castle:"
            piece = "R"  # Thanks, April!
        elif p[:2] == 'KI':
            message = "Your piece is a King:"
            piece = "K"
        elif p[:2] == 'KN':
            message = "Your piece is a Knight:"
            piece = "N"
        elif p[0] in valid_pieces:
            message = f"Your piece is a {valid_pieces[valid_pieces.index(p[0]) + 1]}:"
            piece = piece.upper()[0]
        valid = 1
        return message, piece, valid
    else:
        return "Not a piece"


def piece_color_input_flask(app_color):
    # Get valid color from user
    valid = 0
    message = "Error in chessboard.piece_color_input_flask"
    if not app_color:
        message = "Enter the input indicated."
        color = 0
        return message, color, valid
    color = app_color.upper()[0]
    if not color.isalpha():
        message = "Enter color names with only letters."
    elif (color[0] != 'B') and (color[0] != 'W'):  # TODO: delete index
        message = "Enter \"Black\" or \"White.\""
    elif color.isalpha() and ((color[0] == 'B') or (color[0] == 'W')):  # TODO: delete index
        if color[0] == "B":
            message = "Your piece is Black:"
        if color[0] == "W":
            message = "Your piece is White:"
        valid = 1
    return message, color, valid


def locator_row_flask(app_row, piece, color):
    valid = 0
    message = "Error in chessboard.locator_row_flask"
    if not app_row.isdigit():
        message = "Enter the input indicated."
    elif not 0 < int(app_row) < 9:
        message = "You have to be on the board to play."
    elif piece == 'P' and color == 'W':
        if int(app_row) < 2:
            message = "White pawns can't be on that row"
        if 2 <= int(app_row) <= 7:
            message = f"You're on row {app_row}."
            valid = 1
        if int(app_row) > 7:
            message = "You must promote to a queen, rook, bishop, or knight."
    elif piece == 'P' and color == 'B':
        if int(app_row) > 7:
            message = "Black pawns can't be on that row"
        if 2 <= int(app_row) <= 7:
            message = f"You're on row {app_row}."
            valid = 1
        if int(app_row) < 2:
            message = "You must promote to a queen, rook, bishop, or knight."
    else:
        message = f"You're on row {app_row}."
        valid = 1
    return message, app_row, valid


def locator_column_flask(app_column, app_row):
    valid = 0
    if not app_column:
        message = "Enter the input indicated."
        raw_column = 0
        position = 0
        return message, raw_column, position, valid
    raw_column = app_column.upper()[0]
    position = 0
    if not raw_column.isalpha():
        message = "Enter the input indicated."
        return message, raw_column, position, valid
    elif raw_column not in string.ascii_uppercase[0:8]:
        message = "You have to be on the board to play."
        return message, raw_column, position, valid
    else:
        message = f"You're on column {raw_column}."
        valid = 1

    column = (list(string.ascii_uppercase).index(raw_column)) + 1
    position = (app_row - 1) * 8 + column
    return message, raw_column, position, valid


def locate_pieces(piece, position, color):
    #  summon piece functions from "chess_functions.py":
    if piece != 'P':
        capture = {None}
    if piece == 'N':
        attacked = chess_functions.knight(position)
    if piece == 'B':
        attacked = chess_functions.bishop(position)
    if piece == 'R':
        attacked = chess_functions.rook(position)
    if piece == 'Q':
        attacked = chess_functions.queen(position)
    if piece == 'K':
        attacked = chess_functions.king(position, color)
    if piece == 'P' and color == 'B':
        if 8 < position < 57:
            attacked = chess_functions.black_pawn(position)[0]
            capture = chess_functions.black_pawn(position)[1]
        else:
            attacked = chess_functions.black_pawn(position)
            capture = {None}
    if piece == 'P' and color == 'W':
        if 57 > position > 8:
            attacked = chess_functions.white_pawn(position)[0]
            capture = chess_functions.white_pawn(position)[1]
        else:
            attacked = chess_functions.white_pawn(position)
            capture = {None}
    return attacked, capture


def make_print_piece(piece, color):
    # use chess font
    print_piece = ""
    if piece == "K":
        print_piece = pieces[0]
    if piece == "Q":
        print_piece = pieces[1]
    if piece == "B":
        print_piece = pieces[2]
    if piece == "N":
        print_piece = pieces[3]
    if piece == "R":
        print_piece = pieces[4]
    if piece == "P":
        print_piece = pieces[5]
    if color == "B":
        print_piece = pieces[pieces.index(print_piece) + 6]
    return print_piece


def print_board_file(print_piece, position, attacked, capture):
    # prints contents into text file to be read as HTML
    row = 8
    color = "light"
    ref_square = 56
    with open('boardroom.txt', 'w', encoding='utf-8') as file:
        while row > 0:
            file.write("<tr>")
            file.write(''.join(["<th>", str(row), "</th>"]))
            for square in range(1, 9):
                file.write(''.join(["<td class=\"", color, "\">"]))
                if square + ref_square == position:
                    file.write(print_piece)
                elif square + ref_square in attacked:
                    file.write("X")
                elif square + ref_square in capture:
                    file.write("C")
                file.write("</td>")
                if color == "light":
                    color = "dark"
                elif color == "dark":
                    color = "light"
            file.write("</tr>")
            if color == "light":
                color = "dark"
            elif color == "dark":
                color = "light"
            row -= 1
            ref_square -= 8
        file.write("<tr>")
        file.write("<th></th>")
        ltr_index = 0
        for col in range(8):
            file.write(''.join(["<th>", ascii_uppercase[ltr_index], "</th>"]))
            ltr_index += 1
        file.write("</tr>")


def print_board_stdout(print_piece, position, attacked, capture):
    # print_board console output version. Use with io and contextlib modules.
    # prints contents into variable to be read as HTML
    row = 8
    color = "light"
    ref_square = 56
    while row > 0:
        print("<tr>")
        print("<th>", row, "</th>", sep="")
        for square in range(1, 9):
            print("<td class=\"", color, "\">", sep="", end="")
            if square + ref_square == position:
                print(print_piece, sep="", end="")
            elif square + ref_square in attacked:
                print("X", sep="", end="")
            elif square + ref_square in capture:
                print("C", sep="", end="")
            print("</td>", sep="")
            if color == "light":
                color = "dark"
            elif color == "dark":
                color = "light"
        print("</tr>")
        if color == "light":
            color = "dark"
        elif color == "dark":
            color = "light"
        row -= 1
        ref_square -= 8
    print("<tr>")
    print("<th></th>")
    ltr_index = 0
    for col in range(8):
        print("<th>", ascii_uppercase[ltr_index], "</th>", sep="")
        ltr_index += 1
    print("</tr>")
