from Figure import Figure


class Knight(Figure):
    def can_move(self, board, row, col, row1, col1):
        if row1 == row and col == col1:
            return False
        if abs(row1 - row) == abs(col1 - col):
            return False  # конь не может ходить по диагонали
        return {abs(row1 - row), abs(col1 - col)} == {1, 2}  # проверка,
        # что ход был сделан буквой Г

    def __str__(self):
        return super().__str__() + 'N'
