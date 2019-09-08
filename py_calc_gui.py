from py_calc import calculate
from tkinter import *

# Количество ячеек в сетке расположения элементов окна
CELL_X_COUNT = 7
CELL_Y_COUNT = 5

# Размеры отдельных ячеек сетки
CELL_X_SIZE = 100
CELL_Y_SIZE = 100

# Ширина границы между кнопками
BORDER = 4


# Функция создает окно приложения
def create_window():
    frm = Tk()
    frm.title('PyCalc')

    w_window = CELL_X_COUNT * CELL_X_SIZE
    h_window = CELL_Y_COUNT * CELL_Y_SIZE

    w_screen = frm.winfo_screenwidth()
    h_screen = frm.winfo_screenheight()
    x_pos = (w_screen // 2) - (w_window // 2)
    y_pos = (h_screen // 2) - (h_window // 2)

    frm.geometry(str(w_window) + "x" + str(h_window) + "+" + str(x_pos) + "+" + str(y_pos))
    frm.minsize(w_window, h_window)
    frm.maxsize(w_window, h_window)

    return frm


# Функция создает кнопки
def create_buttons(frm):
    button_names = ['CE', '^', 'sin', '7', '8', '9', '+',
                    'cos', 'tan', 'cotan', '4', '5', '6', '-',
                    'abs', 'ln', 'log', '1', '2', '3', '*',
                    'lg', 'sqrt', 'exp', '0', '.', '=', '/']
    buttons = []
    r = 0
    c = 0
    for btn_name in button_names:
        buttons.append(Button(frm, text=btn_name, font='Arial 14'))
        buttons[-1].place(x=c * CELL_X_SIZE + BORDER, y=(r + 1) * CELL_Y_SIZE + BORDER,
                          width=CELL_X_SIZE - (2 * BORDER),
                          height=CELL_Y_SIZE - (2 * BORDER))
        c += 1
        if c == CELL_X_COUNT:
            c = 0
            r += 1


# Функция создает дисплей
def create_display(frm):
    display = Entry(frm, font='Arial 18', justify='right')
    display.place(x=BORDER, y=BORDER + (CELL_Y_SIZE // 4), width=(CELL_X_COUNT * CELL_X_SIZE) - (BORDER * 2),
                  height=(CELL_Y_SIZE // 2) - BORDER)


# Здесь начинается выполнение программы
root = create_window()
create_buttons(root)
create_display(root)

Tk.mainloop(root)