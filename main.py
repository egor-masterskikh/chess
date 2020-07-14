from PIL import ImageTk, Image
import tkinter
from figures.Board import Board
from figures.Colors import *

SQUARE_SIZE = 90
BORDER_THICKNESS = 3
BORDER_COLOR_DEF = "black"
BORDER_COLOR_ACTIVE = "green"

tk = tkinter.Tk()
tk.wm_title("Chess")

# ********************************ИЗОБРАЖЕНИЯ********************************
IMAGE_SIZE = (SQUARE_SIZE - 2 * BORDER_THICKNESS, SQUARE_SIZE - 2 * BORDER_THICKNESS)
WK = ImageTk.PhotoImage(Image.open("images/png/wking.png").resize(IMAGE_SIZE))
BK = ImageTk.PhotoImage(Image.open("images/png/bking.png").resize(IMAGE_SIZE))
WQ = ImageTk.PhotoImage(Image.open("images/png/wqueen.png").resize(IMAGE_SIZE))
BQ = ImageTk.PhotoImage(Image.open("images/png/bqueen.png").resize(IMAGE_SIZE))
WB = ImageTk.PhotoImage(Image.open("images/png/wbishop.png").resize(IMAGE_SIZE))
BB = ImageTk.PhotoImage(Image.open("images/png/bbishop.png").resize(IMAGE_SIZE))
WN = ImageTk.PhotoImage(Image.open("images/png/wknight.png").resize(IMAGE_SIZE))
BN = ImageTk.PhotoImage(Image.open("images/png/bknight.png").resize(IMAGE_SIZE))
WR = ImageTk.PhotoImage(Image.open("images/png/wrook.png").resize(IMAGE_SIZE))
BR = ImageTk.PhotoImage(Image.open("images/png/brook.png").resize(IMAGE_SIZE))
WP = ImageTk.PhotoImage(Image.open("images/png/wpawn.png").resize(IMAGE_SIZE))
BP = ImageTk.PhotoImage(Image.open("images/png/bpawn.png").resize(IMAGE_SIZE))
EMPTY = ImageTk.PhotoImage(Image.new("RGB", IMAGE_SIZE, "white"))
# ********************************ИЗОБРАЖЕНИЯ********************************

# ********************************ВИДЖЕТЫ********************************
WK_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=WK)'
BK_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=BK)'
WQ_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=WQ)'
BQ_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=BQ)'
WB_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=WB)'
BB_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=BB)'
WN_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=WN)'
BN_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=BN)'
WR_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=WR)'
BR_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=BR)'
WP_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=WP)'
BP_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=BP)'
E_LB = 'tkinter.Label(tk, width=SQUARE_SIZE, height=SQUARE_SIZE, bg=BORDER_COLOR_DEF, image=EMPTY)'
# ********************************ВИДЖЕТЫ********************************

WHITE_FIGURES_IMAGES = {'Pawn': (WP, WP_LB), 'Knight': (WN, WN_LB), 'Bishop': (WB, WB_LB),
                        'Rook': (WR, WR_LB), 'Queen': (WQ, WQ_LB), 'King': (WK, WK_LB)}
BLACK_FIGURES_IMAGES = {'Pawn': (BP, BP_LB), 'Knight': (BN, BN_LB), 'Bishop': (BB, BB_LB),
                        'Rook': (BR, BR_LB), 'Queen': (BQ, BQ_LB), 'King': (BK, BK_LB)}


def update_board():
    for i, row in enumerate(board.field[::-1]):
        for j, el in enumerate(row):
            if el is None:
                boardTk[i][j]['image'] = EMPTY
            elif el.color == WHITE:
                boardTk[i][j]['image'] = WHITE_FIGURES_IMAGES[el.__class__.__name__][0]
            else:
                boardTk[i][j]['image'] = BLACK_FIGURES_IMAGES[el.__class__.__name__][0]


def choose_figure(event):
    global pawn_coords
    wdg = event.widget
    row, col, row1, col1 = pawn_coords
    if wdg['text'] == 'Q':
        board.move_and_promote_pawn(7 - row, col, 7 - row1, col1, 'Q')
    elif wdg['text'] == 'R':
        board.move_and_promote_pawn(7 - row, col, 7 - row1, col1, 'R')
    elif wdg['text'] == 'B':
        board.move_and_promote_pawn(7 - row, col, 7 - row1, col1, 'B')
    else:
        board.move_and_promote_pawn(7 - row, col, 7 - row1, col1, 'N')
    chooser_q.grid_forget()
    chooser_r.grid_forget()
    chooser_b.grid_forget()
    chooser_n.grid_forget()
    chooser_q.unbind('<Button-1>')
    chooser_r.unbind('<Button-1>')
    chooser_b.unbind('<Button-1>')
    chooser_n.unbind('<Button-1>')
    for r in boardTk:
        for label in r:
            label.bind('<Button-1>', move)
    pawn_coords = None
    base_actions()


def move(event):
    global from_wdg, pawn_coords
    wdg = event.widget
    row1, col1 = wdg.grid_info()['row'], wdg.grid_info()['column']
    if from_wdg is None:
        from_wdg = wdg
        wdg['bg'] = BORDER_COLOR_ACTIVE
    elif from_wdg is not None and (from_wdg.grid_info()['row'], from_wdg.grid_info()['column']) == \
            (row1, col1):
        from_wdg = None
        wdg['bg'] = BORDER_COLOR_DEF
    else:
        row, col = from_wdg.grid_info()["row"], from_wdg.grid_info()["column"]
        if board.castle(7 - row, col, 7 - row1, col1) or \
                board.check_pawn_promotion(7 - row, col, 7 - row1, col1) or \
                board.move_piece(7 - row, col, 7 - row1, col1):
            info_label["text"] = "Success."
            if board.check_pawn_promotion(7 - row, col, 7 - row1, col1):
                pawn_coords = row, col, row1, col1
                chooser_q.grid(row=3, column=9)
                chooser_r.grid(row=4, column=9)
                chooser_b.grid(row=5, column=9)
                chooser_n.grid(row=6, column=9)
                chooser_q.bind('<Button-1>', choose_figure)
                chooser_r.bind('<Button-1>', choose_figure)
                chooser_b.bind('<Button-1>', choose_figure)
                chooser_n.bind('<Button-1>', choose_figure)
                for r in boardTk:
                    for label in r:
                        label.unbind('<Button-1>')
                return
            # print(7 - row, col, 7 - row1, col1, sep='')
        else:
            info_label['text'] = "Incorrect move."
        base_actions()


def base_actions():
    global from_wdg
    info_label["text"] += f""" {"White's" if board.color == WHITE else "Black's"} move"""
    from_wdg["bg"] = BORDER_COLOR_DEF
    from_wdg = None
    update_board()
    verdict = board.check()
    if verdict:
        info_label['text'] = verdict
        pass


# ********************************ВИДЖЕТЫ********************************
info_label = tkinter.Label(tk, bg="green", text="White's move", fg="white", font="arial 20")
info_label.grid(row=0, column=8, columnspan=4)
chooser_q = tkinter.Label(tk, bg="red", text="Q", fg="white", font="arial 22")
chooser_b = tkinter.Label(tk, bg='blue', text='B', fg="white", font='arial 22')
chooser_r = tkinter.Label(tk, bg='green', text='R', fg="white", font='arial 22')
chooser_n = tkinter.Label(tk, bg='orange', text='N', fg="white", font='arial 22')
# ********************************ВИДЖЕТЫ********************************

from_wdg = None
pawn_coords = None
board = Board()
boardTk = []


def main():
    for i, row in enumerate(board.field[::-1]):
        boardTk.append([])
        for j, el in enumerate(row):
            if el is None:
                new_lb = eval(E_LB)
            elif el.color == WHITE:
                new_lb = eval(WHITE_FIGURES_IMAGES[el.__class__.__name__][1])
            else:
                new_lb = eval(BLACK_FIGURES_IMAGES[el.__class__.__name__][1])
            boardTk[-1].append(new_lb)
            new_lb.bind('<Button-1>', move)
            new_lb.grid(row=i, column=j)


main()
tk.mainloop()
