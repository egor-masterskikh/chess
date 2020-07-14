from Figure import Figure


class Rook(Figure):
    def __init__(self, color):
        self.moved = False
        super().__init__(color)

    def can_move(self, board, row, col, row1, col1):
        if row1 == row and col == col1:
            return False
        # Невозможно сделать ход в клетку,
        # которая не лежит в том же ряду или столбце клеток.
        if not (row == row1 or col == col1):
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if board.field[r][col] is not None:
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if board.field[row][c] is not None:
                return False
        return True

    def __str__(self):
        return super().__str__() + 'R'
