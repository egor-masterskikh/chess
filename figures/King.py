from Figure import Figure
from itertools import product
from Colors import opponent


class King(Figure):
    def __init__(self, color):
        self.moved = False  # переменная для проверки возможности рокировки
        super().__init__(color)

    def can_move(self, board, row, col, row1, col1):
        return not (row1 == row and col == col1) and abs(row - row1) in (0, 1) and \
               abs(col - col1) in (0, 1)

    def is_under_attack(self, board, row, col):
        """Возвращает True, если хотя бы одна фигура противника при ходе короля в клетку
        (row, col) сможет его атаковать"""
        for i, j in product(range(8), repeat=2):
            p = board.field[i][j]
            if isinstance(p, Figure) and p.color == opponent(self.color) and \
                    p.can_attack(board, i, j, row, col):
                return True
        return False

    def __str__(self):
        return super().__str__() + 'K'
