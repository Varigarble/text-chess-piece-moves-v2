from flask import Flask, render_template, request, redirect, session, url_for
import chessboard
import io
import os
from contextlib import redirect_stdout


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')
    if app.secret_key:
        print('using Heroku Config Vars')
    else:
        app.secret_key = "local-test-password-123"
        print('using local Secret Key')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    piece = None
    color = None
    row = None
    column = None
    position = None

    @app.route("/", methods=['GET', 'POST'])
    def entry_page():
        nonlocal piece, color, row, column, position
        piece, color, row, column, position = None, None, None, None, None
        return render_template(
            "chess-input-0.html"
        )

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
            session["piece"] = message_piece[1]
            piece = session["piece"]
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
        nonlocal color
        piece = session["piece"]
        message = "Color Input:"
        valid = 0
        if request.method == "POST":
            message_color = chessboard.piece_color_input_flask(request.form.get("content"))
            message = message_color[0]
            session["color"] = message_color[1]
            color = session["color"]
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
        nonlocal row
        piece = session["piece"]
        color = session["color"]
        message = "Row Input:"
        valid = 0
        if request.method == "POST":
            message_row = chessboard.locator_row_flask(request.form.get("content"), piece, color)
            message = message_row[0]
            session["row"] = message_row[1]
            row = session["row"]
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
        nonlocal column
        nonlocal position
        piece = session["piece"]
        color = session["color"]
        row = session["row"]
        message = "Column Input:"
        valid = 0
        if request.method == "POST":
            message_col = chessboard.locator_column_flask(request.form.get("content"), int(row))
            message = message_col[0]
            session["column"] = message_col[1]
            column = session["column"]
            session["position"] = message_col[2]
            position = session["position"]
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
        piece = session["piece"]
        color = session["color"]
        row = session["row"]
        column = session["column"]
        position = session["position"]
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

    @app.route("/session_clear")
    def clear():
        print(session)
        session.clear()
        print(session)  # verify session cleared
        piece, color, row, column, position = None, None, None, None, None
        print(piece, color, row, column, position)  # verify variables cleared
        return redirect(url_for("entry_page"))

    return app
