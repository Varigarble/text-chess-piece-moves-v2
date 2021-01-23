""" This is a library of standard chess pieces and functions showing the possible moves of each."""


def white_pawn(position):

    attacked = {None}
    capture = {None}

    if 56 < position < 65:
        print("You must promote to a new queen, rook, bishop or knight")

    if 8 < position < 57:
        attacked.add(position + 8)
        if ((position + 7) % 8) != 0:
            capture.add(position + 7)
        if ((position + 8) % 8) != 0:
            capture.add(position + 9)
    if 8 < position < 17:
        attacked.add(position + 16)

    return attacked, capture


def black_pawn(position):

    attacked = {None}
    capture = {None}

    if 0 < position < 9:
        print("You must promote to a new queen, rook, bishop or knight")
    if 8 < position < 57:
        attacked.add(position - 8)
        if ((position - 8) % 8) != 0:
            capture.add(position - 7)
        if ((position - 9) % 8) != 0:
            capture.add(position - 9)
    if 48 < position < 57:
        attacked.add(position - 16)

    return attacked, capture


def rook(position):
    reset_position = position
    attacked = {None}
    while (position > 1) and (position - 1) % 8 != 0:
        attacked.add(position - 1)
        position -= 1
    position = reset_position

    while (position < 64) and (position % 8 != 0):
        attacked.add(position + 1)
        position += 1
    position = reset_position
    while ((position - 8) > 0) and (position > 8):
        attacked.add(position - 8)
        position -= 8
    position = reset_position
    while (position + 8) < 65:
        attacked.add(position + 8)
        position += 8
    return attacked


def bishop(position):
    reset_position = position
    attacked = {None}

    # ll to ur diagonal
    while (position > 1) and (position < 65) and (((position - 1) % 8) != 0):
        if (position - 9) > 0:
            attacked.add(position - 9)
        position -= 9
    position = reset_position
    while (position > 0) and (position < 64) and ((position % 8) != 0):
        if (position + 9) < 65 and ((position + 9) > position % 8):
            attacked.add(position + 9)
        position += 9
    position = reset_position

    # ul to lr diagonal
    while (position > 1) and (position < 64) and ((position % 8) != 0):
        if (position - 7) > 0:
            attacked.add(position - 7)
        position -= 7
    position = reset_position
    while (position > 1) and (position < 64) and (((position + 7) % 8) != 0):
        if (position + 7) < 65:
            attacked.add(position + 7)
        position += 7
    return attacked


def queen(position):
    attacked = rook(position) | bishop(position)
    return attacked


def knight(position):

    reset_position = position
    attacked = {None}

    # vertical up & left/right
    if (((position + 15) % 8) != 0) and (position + 15 < 64):
        attacked.add(position + 15)
    position = reset_position
    if (((position + 16) % 8) != 0) and (position + 17 <= 64):
        attacked.add(position + 17)
    position = reset_position

    # horizontal left & up/down
    if (((position - 1) % 8) != 0) and (((position - 2) % 8) != 0) \
            and (2 < position < 57):
        attacked.add(position + 6)
    position = reset_position
    if (((position - 1) % 8) != 0) and (((position - 2) % 8) != 0) \
            and (10 < position < 65):
        attacked.add(position - 10)
    position = reset_position

    # horizontal right & up/down
    if ((position % 8) != 0) and (((position + 1) % 8) != 0) \
            and (position < 55):
        attacked.add(position + 10)
    position = reset_position
    if ((position % 8) != 0) and (((position + 1)) % 8 != 0) \
            and (8 < position < 63):
        attacked.add(position - 6)
    position = reset_position

    # vertical down & left/right
    if (((position - 17) % 8) != 0) and (position - 17 > 0):
        attacked.add(position - 17)
    position = reset_position
    if (((position - 16) % 8) != 0) and (position - 15 > 1):
        attacked.add(position - 15)

    return attacked


def king(position, color):
    attacked = {None}
    # top row
    if ((position + 7) < 64) and (((position + 7) % 8) != 0):
        attacked.add(position + 7)
    if (position + 8) < 65:
        attacked.add(position + 8)
    if ((position % 8) != 0) and (position < 56):
        attacked.add(position + 9)
    # left/right
    if (((position - 1) % 8) != 0) and (position > 1):
        attacked.add(position - 1)
    if ((position % 8) != 0) and (position < 64):
        attacked.add(position + 1)
    # bottom row
    if (((position - 9) % 8) != 0) and ((position - 9) > 0):
        attacked.add(position - 9)
    if (position - 8) > 0:
        attacked.add(position - 8)
    if ((position % 8) != 0) and (position > 9):
        attacked.add(position - 7)
    # castle
    if (position == 61) and (color == 'B'):
        attacked.add(63)
        attacked.add(59)
    if (position == 5) and (color == 'W'):
        attacked.add(7)
        attacked.add(3)
    return attacked
