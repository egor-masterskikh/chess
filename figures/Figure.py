from Colors import WHITE


class Figure:
    def __init__(self, color):
        self.color = color

    def can_attack(self, board, row, col, row1, col1):
        # для всех фигур, кроме пешки, этот метод эквивалентен методу can_move данной фигуры
        # для пешки данный метод переопределен под взятие на проходе
        return self.can_move(board, row, col, row1, col1)

    def can_move(self, board, row, col, row1, col1):
        return

    def __str__(self):
        return 'w' if self.color == WHITE else 'b'
