from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from Rook import Rook
from Pawn import Pawn
from King import King
from Figure import Figure
from itertools import product
from Colors import *


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = [[Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                       King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
                      [Pawn(WHITE)] * 8,
                      [None] * 8,
                      [None] * 8,
                      [None] * 8,
                      [None] * 8,
                      [Pawn(BLACK)] * 8,
                      [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                       King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]]
        # self.field = [[None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None],
        #               [None, None, None, None, None, None, None, None]]
        self.kings_coords = {BLACK: (7, 4), WHITE: (0, 4)}  # координаты королей нужны для
        # отслеживания шаха, мата и пата

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста, то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        return str(piece)

    def _can_move_piece(self, row, col, row1, col1):
        """Возвращает True, если возможно сделать ход из клетки (row, col) в клетку (row1, col1)"""
        if not (0 <= row < 8 and 0 <= col < 8) or not (0 <= row1 < 8 and 0 <= col1 < 8):
            return False  # нельзя пойти все доски
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False  # нельзя пойти из пустого места
        if piece.color != self.color:
            return False  # сейчас ходят фигуры другого цвета

        if self.field[row1][col1] is None:  # если это не атака
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].color == opponent(piece.color):  # если это атака
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:  # если была сделана попытка атаковать свою фигуру
            return False
        return not self.king_under_attack(row, col, row1, col1)

    def king_under_attack(self, row, col, row1, col1):
        from_piece = self.field[row][col]
        to_piece = self.field[row1][col1]
        self.field[row][col], self.field[row1][col1] = None, from_piece
        if isinstance(from_piece, King):
            king_x, king_y = row1, col1
        else:
            king_x, king_y = self.kings_coords[self.color]
        king = self.field[king_x][king_y]
        if king.is_under_attack(self, king_x, king_y):
            # исключает возможность хода связанной с королем фигуры и бездействия при шахе
            self.field[row][col], self.field[row1][col1] = from_piece, to_piece
            return True
        else:
            self.field[row][col], self.field[row1][col1] = from_piece, to_piece
            return False

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет - вернёт False"""
        piece = self.field[row][col]
        if self._can_move_piece(row, col, row1, col1):
            self.field[row][col], self.field[row1][col1] = None, piece
            if isinstance(piece, Rook) and not isinstance(piece, Queen):
                # если передвинули ладью или короля, то помечаем, что эта фигура уже двигалась =>
                # рокировка с этой фигурой невозможна
                piece.moved = True
            elif isinstance(piece, King):
                piece.moved = True
                self.kings_coords[self.color] = (row1, col1)
                # перезаписываем текущие координаты короля
            self.color = opponent(self.color)
            return True
        return False

    def check(self):
        """Проверяет шах, чтобы затем проверить пат или мат"""
        king_x, king_y = self.kings_coords[self.color]
        king = self.field[king_x][king_y]
        if king.is_under_attack(self, king_x, king_y):
            return f'Checkmate! {"White" if self.color == BLACK else "Black"} won.' \
                if self._checkmate() else False
        else:
            return 'Draw!' if self._pat() else False

    def _pat(self):
        """Возвращает True, если текущая позиция - пат. В противном случае возвращает False"""
        for r, c in product(range(8), repeat=2):
            piece = self.field[r][c]
            if isinstance(piece, Figure) and piece.color == self.color:
                for r1, c1 in product(range(8), repeat=2):
                    if self._can_move_piece(r, c, r1, c1):
                        return False
        return True

    def _checkmate(self):
        return self._pat()

    def move_and_promote_pawn(self, row, col, row1, col1, char='Q'):
        """Превращение пешки в ферзя, слона, ладью или коня"""
        if char in ('Q', 'B', 'N', 'R'):
            self.field[row][col] = None
            if char == 'Q':
                self.field[row1][col1] = Queen(self.color)
            elif char == 'B':
                self.field[row1][col1] = Bishop(self.color)
            elif char == 'N':
                self.field[row1][col1] = Knight(self.color)
            elif char == 'R':
                self.field[row1][col1] = Rook(self.color)
            self.color = opponent(self.color)
            return True
        return False

    # проведение пешки разделено на 2 метода, поскольку после проверки условия проведения пешки
    # мы должны убедиться, запрашивать ли у пользователя букву фигуры для превращения или нет
    def check_pawn_promotion(self, row, col, row1, col1):
        """Проверяет условия проведения пешки на конец доски"""
        pawn = self.field[row][col]
        if not (isinstance(pawn, Pawn) and self._can_move_piece(row, col, row1, col1)):
            return False
        return pawn.color == BLACK and row1 == 0 or pawn.color == WHITE and row1 == 7

    def castle(self, row, col, row1, col1):
        if row != row1 or abs(col - col1) != 2:
            return False
        king = self.field[row][col]
        if not isinstance(king, King):
            return False
        rook_col = 0 if col1 == 2 else 7
        rook = self.field[row][rook_col]
        if not isinstance(rook, Rook) or isinstance(rook, Queen):
            return False
        if rook.moved or king.moved:
            return False
        if rook_col == 7 and self.field[row][5:7] != [None, None]:
            return False
        if rook_col == 0 and self.field[row][1:4] != [None, None, None]:
            return False
        if self.king_under_attack(row, col, row1, col1):
            return False
        # наконец можно рокироваться
        self.field[row][col], self.field[row][col1] = None, king
        if rook_col == 7:
            self.field[row][rook_col], self.field[row][5] = None, rook
        else:
            self.field[row][rook_col], self.field[row][3] = None, rook
        king.moved, rook.moved = True, True
        self.kings_coords[self.color] = row, col1
        self.color = opponent(self.color)
        return True
