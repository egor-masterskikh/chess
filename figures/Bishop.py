from Figure import Figure


class Bishop(Figure):
    def can_move(self, board, row, col, row1, col1):
        # если слон пытается пойти не по диагонали
        if row1 == row and col == col1:
            return False
        if abs(row - row1) != abs(col - col1):
            return False
        step_row = 1 if (row1 > row) else -1
        step_col = 1 if (col1 > col) else -1
        for i in range(1, abs(row1 - row)):
            # Если на пути по горизонтали есть фигура
            if board.field[row + step_row * i][col + step_col * i] is not None:
                return False
        return True

    def __str__(self):
        return super().__str__() + 'B'
