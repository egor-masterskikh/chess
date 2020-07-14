from Figure import Figure
from Colors import WHITE


class Pawn(Figure):
    def can_move(self, board, row, col, row1, col1):
        if row1 == row and col == col1:
            return False
        if col != col1:
            return False
        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        # ход на 1 клетку
        if row + direction == row1:
            return True
        # ход на 2 клетки
        if (row == start_row and row + 2 * direction == row1 and
                board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        """Проверяется возможность взятия на проходе"""
        direction = 1 if self.color == WHITE else -1
        return row + direction == row1 and (col + 1 == col1 or col - 1 == col1)

    def __str__(self):
        return super().__str__() + 'P'
