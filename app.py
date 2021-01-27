from flask import Flask, render_template, request, redirect, session, url_for
import chessboard
import io
import os
from contextlib import redirect_stdout


def create_app():
    app = Flask(__name__)
    # get Heroku Config Vars to utilize Flask session
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'  # set to utilize Flask session
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    @app.route("/", methods=['GET', 'POST'])
    def entry_page():
        # Start page. Restart button destination.
        return render_template(
            "chess-input-0.html"
        )

    # read empty chessboard table from file and store for html rendering
    with open("empty_chessboard.txt", 'r', encoding='utf-8') as f:
        empty_board = f.read()

    @app.route("/chess-input-1", methods=['GET', 'POST'])
    def input_page_1():
        # get piece from user
        piece = None
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
        # get color from user
        piece = session["piece"]
        color = None
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
        # get row from user
        piece = session["piece"]
        color = session["color"]
        row = None
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
        # get column from user, calculate position
        piece = session["piece"]
        color = session["color"]
        row = session["row"]
        column = None
        position = None
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
        # clear session cookie data & start over
        session.clear()
        return redirect(url_for("entry_page"))

    return app
