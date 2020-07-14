from Bishop import Bishop
from Rook import Rook
from Colors import WHITE


class Queen(Rook, Bishop):
    def can_move(self, board, row, col, row1, col1):
        # совмещает в себе свойства Слона и Ладьи
        return Bishop.can_move(self, board, row, col, row1, col1) or \
               Rook.can_move(self, board, row, col, row1, col1)

    def __str__(self):
        return ('w' if self.color == WHITE else 'b') + 'Q'
