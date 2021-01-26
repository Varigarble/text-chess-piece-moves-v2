from flask import Flask, render_template, request, redirect, session, url_for
import chessboard
import io
import os
import redis
from contextlib import redirect_stdout


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')
    if app.secret_key:
        print('using Heroku Config Vars')
    else:
        app.secret_key = "local-test-password-123"
        print('using local Secret Key')
    r = redis.from_url(os.environ.get('REDIS_URL'), charset="utf-8", decode_responses=True)
    # r = redis.Redis(host='localhost', port=6379, db=0)
    app.config['SESSION_TYPE'] = 'redis'
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # piece = None
    # color = None
    # row = None
    # column = None
    # position = None

    @app.route("/", methods=['GET', 'POST'])
    def entry_page():
        # nonlocal piece, color, row, column, position
        # piece, color, row, column, position = None, None, None, None, None
        return render_template(
            "chess-input-0.html"
        )

    with open("empty_chessboard.txt", 'r', encoding='utf-8') as f:
        empty_board = f.read()

    @app.route("/chess-input-1", methods=['GET', 'POST'])
    def input_page_1():
        # nonlocal piece
        # print("page 1 load piece: ", piece)
        message = None
        valid = 0
        if request.method == "POST":
            message_piece = chessboard.piece_name_input_flask(request.form.get("content"))
            message = message_piece[0]
            # session["piece"] = message_piece[1]
            # piece = session["piece"]
            r.set('piece', message_piece[1])
            piece = r.get('piece')
            print("page 1 set piece: ", piece)  # del
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
        # nonlocal color
        # print("page 2 load color: ", color)
        # piece = session["piece"]
        piece = r.get('piece')
        print("page 2 load piece: ", piece)
        message = "Color Input:"
        valid = 0
        if request.method == "POST":
            message_color = chessboard.piece_color_input_flask(request.form.get("content"))
            message = message_color[0]
            # session["color"] = message_color[1]
            # color = session["color"]
            r.set('color', message_color[1])
            color = r.get('color')
            print("page 2 set color: ", color)
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
        # nonlocal row
        # print("page 3 load row: ", row)
        # piece = session["piece"]
        # color = session["color"]
        piece = r.get('piece')
        print("page 3 load piece: ", piece)
        color = r.get('color')
        print("page 3 load color: ", color)
        message = "Row Input:"
        valid = 0
        if request.method == "POST":
            message_row = chessboard.locator_row_flask(request.form.get("content"), piece, color)
            message = message_row[0]
            # session["row"] = message_row[1]
            # row = session["row"]
            r.set('row', message_row[1])
            row = r.get('row')
            print("page 3 set row: ", row)
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
        # nonlocal column
        # nonlocal position
        # print("page 4 load column: ", column)
        # print("page 4 load position: ", position)
        # piece = session["piece"]
        # color = session["color"]
        # row = session["row"]
        piece = r.get('piece')
        print("page 4 load piece: ", piece)
        color = r.get('color')
        print("page 4 load color: ", color)
        row = r.get('row')
        print("page 4 load row: ", row)
        message = "Column Input:"
        valid = 0
        if request.method == "POST":
            message_col = chessboard.locator_column_flask(request.form.get("content"), int(row))
            message = message_col[0]
            # session["column"] = message_col[1]
            # column = session["column"]
            r.set('column', message_col[1])
            column = r.get('column')
            print("page 4 set column: ", column)
            # session["position"] = message_col[2]
            # position = session["position"]
            r.set('position', message_col[2])
            position = r.get('position')
            print("page 4 set position: ", position)
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
        # piece = session["piece"]
        # color = session["color"]
        # row = session["row"]
        # column = session["column"]
        # position = session["position"]
        piece = r.get('piece')
        color = r.get('color')
        row = r.get('row')
        column = r.get('column')
        position = int(r.get('position'))
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
        # print(session)
        # session.clear()
        # print(session)  # verify session cleared
        r.delete("piece", "color", "row", "column", "position")
        r.set("piece", 0)
        r.set("color", 0)
        r.set("row", 0)
        r.set("column", 0)
        r.set("position", 0)
        piece, color, row, column, position = None, None, None, None, None
        print(piece, color, row, column, position)  # verify variables cleared
        return redirect(url_for("entry_page"))

    return app
