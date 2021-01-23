from flask import Flask, render_template, request
import chessboard
import io
from contextlib import redirect_stdout


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET', 'POST'])
    def entry_page():
        return render_template(
            "chess-input-0.html"
        )

    piece = None
    color = None
    row = None
    column = None
    position = None
    with open("empty_chessboard.txt", 'r', encoding='utf-8') as f:
        empty_board = f.read()

    @app.route("/chess-input-1", methods=['GET', 'POST'])
    def input_page_1():
        nonlocal piece
        message = None
        valid = 0
        if request.method == "POST":
            message_piece = chessboard.piece_name_input_flask(request.form.get("content"))
            message = message_piece[0]
            piece = message_piece[1]
            valid = message_piece[2]
        if valid != 1:
            valid = "<p>Follow instructions to continue.</p>"
        if valid == 1:
            valid = "<a href=\"chess-input-2\"><button type=\"submit\" class=\"form__submit\">Continue</button></a>"
        return render_template(
            "chess-input-1.html",
            message=message,
            piece=piece,
            valid=valid,
            empty_board=empty_board
        )

    @app.route("/chess-input-2", methods=['GET', 'POST'])
    def input_page_2():
        nonlocal piece
        nonlocal color
        message = "Color Input:"
        valid = 0
        if request.method == "POST":
            message_color = chessboard.piece_color_input_flask(request.form.get("content"))
            message = message_color[0]
            color = message_color[1]
            valid = message_color[2]
        if valid != 1:
            valid = "<p>Follow instructions to continue.</p>"
        if valid == 1:
            valid = "<a href=\"chess-input-3\"><button type=\"submit\" class=\"form__submit\">Continue</button></a>"
        return render_template(
            "chess-input-2.html",
            message=message,
            piece=piece,
            color=color,
            valid=valid,
            empty_board=empty_board
        )

    @app.route("/chess-input-3", methods=['GET', 'POST'])
    def input_page_3():
        nonlocal piece
        nonlocal color
        nonlocal row
        message = "Row Input:"
        valid = 0
        if request.method == "POST":
            message_row = chessboard.locator_row_flask(request.form.get("content"), piece, color)
            message = message_row[0]
            row = message_row[1]
            valid = message_row[2]
        if valid != 1:
            valid = "<p>Follow instructions to continue.</p>"
        if valid == 1:
            valid = "<a href=\"chess-input-4\"><button type=\"submit\" class=\"form__submit\">Continue</button></a>"
        return render_template(
            "chess-input-3.html",
            message=message,
            piece=piece,
            color=color,
            row=row,
            valid=valid,
            empty_board=empty_board
        )

    @app.route("/chess-input-4", methods=['GET', 'POST'])
    def input_page_4():
        nonlocal piece
        nonlocal color
        nonlocal row
        nonlocal column
        nonlocal position
        message = "Column Input:"
        valid = 0
        if request.method == "POST":
            message_col = chessboard.locator_column_flask(request.form.get("content"), int(row))
            message = message_col[0]
            column = message_col[1]
            position = message_col[2]
            valid = message_col[3]
        if valid != 1:
            valid = "<p>Follow instructions to continue.</p>"
        if valid == 1:
            valid = "<a href=\"chess-output\"><button type=\"submit\" class=\"form__submit\">Continue</button></a>"
        return render_template(
            "chess-input-4.html",
            message=message,
            piece=piece,
            color=color,
            row=row,
            column=column,
            position=position,
            valid=valid,
            empty_board=empty_board
        )

    @app.route("/chess-output", methods=['GET', 'POST'])
    def output_page():
        nonlocal piece
        nonlocal color
        nonlocal row
        nonlocal column
        nonlocal position
        message = "Done."
        attacked, capture = chessboard.locate_pieces(piece, position, color)  # calls chess_functions.py
        print_piece = chessboard.make_print_piece(piece, color)
        """use this code if reading from file: 
        chessboard.print_board_file(print_piece, position, attacked, capture)
        with open("boardroom.txt", 'r', encoding='utf-8') as f:
             board = f.read()"""
        with io.StringIO() as buf, redirect_stdout(buf):
            print(chessboard.print_board_stdout(print_piece, position, attacked, capture))
            board = buf.getvalue()[0:-6]
        return render_template(
            "chess-output.html",
            message=message,
            piece=piece,
            color=color,
            row=row,
            column=column,
            position=position,
            board=board
        )
    return app
