import tkinter as tk
from tkinter import messagebox
import random
from tkinter import font as tkfont

# Цветовая схема
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#ffffff"
BUTTON_ACTIVE_COLOR = "#e0e0e0"
X_COLOR = "#ff4444"  # Красный для X
O_COLOR = "#4444ff"  # Синий для O
WIN_COLOR = "#44ff44"  # Зеленый для победной линии
RESET_COLOR = "#dddddd"
TEXT_COLOR = "#333333"

# Настройки игры
DEFAULT_PLAYER_SYMBOL = "X"

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("320x450")
window.configure(bg=BG_COLOR)

# Шрифты
title_font = tkfont.Font(family="Arial", size=16, weight="bold")
button_font = tkfont.Font(family="Arial", size=14)
symbol_font = tkfont.Font(family="Arial", size=24, weight="bold")

# Переменные игры
current_player = DEFAULT_PLAYER_SYMBOL
player_symbol = DEFAULT_PLAYER_SYMBOL
computer_symbol = "O"
buttons = []
game_active = False
win_combination = []


def choose_symbol(symbol):
    global player_symbol, computer_symbol, current_player, game_active
    player_symbol = symbol
    computer_symbol = "O" if symbol == "X" else "X"
    current_player = "X"
    game_active = True
    start_game()
    if current_player == computer_symbol:
        computer_move()


def start_game():
    symbol_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)


def reset_game():
    global current_player, game_active, win_combination
    current_player = "X"
    game_active = True
    win_combination = []

    for row in buttons:
        for button in row:
            button.config(text="", bg=BUTTON_COLOR, state=tk.NORMAL)

    if player_symbol == "O":
        computer_move()


def check_winner():
    global win_combination
    # Проверка строк
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            win_combination = [(i, 0), (i, 1), (i, 2)]
            return True
    # Проверка столбцов
    for i in range(3):
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            win_combination = [(0, i), (1, i), (2, i)]
            return True
    # Проверка диагоналей
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        win_combination = [(0, 0), (1, 1), (2, 2)]
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        win_combination = [(0, 2), (1, 1), (2, 0)]
        return True
    return False


def highlight_winner():
    for (i, j) in win_combination:
        buttons[i][j].config(bg=WIN_COLOR)
    # Блокируем кнопки после победы
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)


def is_draw():
    return all(button["text"] != "" for row in buttons for button in row)


def end_game(message):
    global game_active
    game_active = False
    if check_winner():
        highlight_winner()
    messagebox.showinfo("Игра окончена", message)


def computer_move():
    global current_player

    if not game_active or current_player != computer_symbol:
        return

    available_moves = []
    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                available_moves.append((i, j))

    if available_moves:
        row, col = random.choice(available_moves)
        buttons[row][col]["text"] = computer_symbol
        buttons[row][col].config(fg=O_COLOR if computer_symbol == "O" else X_COLOR)

        if check_winner():
            end_game(f"Компьютер ({computer_symbol}) победил!")
        elif is_draw():
            end_game("Ничья!")
        else:
            current_player = player_symbol


def on_click(row, col):
    global current_player

    if not game_active or buttons[row][col]['text'] != "" or current_player != player_symbol:
        return

    buttons[row][col]['text'] = player_symbol
    buttons[row][col].config(fg=X_COLOR if player_symbol == "X" else O_COLOR)

    if check_winner():
        end_game(f"Игрок ({player_symbol}) победил!")
    elif is_draw():
        end_game("Ничья!")
    else:
        current_player = computer_symbol
        window.after(500, computer_move)


# Фрейм для выбора символа
symbol_frame = tk.Frame(window, bg=BG_COLOR)
tk.Label(symbol_frame, text="Выберите символ", font=title_font, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=15)

button_frame = tk.Frame(symbol_frame, bg=BG_COLOR)
button_frame.pack()

x_btn = tk.Button(button_frame, text="X", font=symbol_font, width=4, fg=X_COLOR,
                  command=lambda: choose_symbol("X"), bg=BUTTON_COLOR, activebackground=BUTTON_ACTIVE_COLOR)
x_btn.pack(side="left", padx=10, pady=5)

o_btn = tk.Button(button_frame, text="O", font=symbol_font, width=4, fg=O_COLOR,
                  command=lambda: choose_symbol("O"), bg=BUTTON_COLOR, activebackground=BUTTON_ACTIVE_COLOR)
o_btn.pack(side="right", padx=10, pady=5)

symbol_frame.pack(fill="both", expand=True)

# Фрейм для игрового поля
game_frame = tk.Frame(window, bg=BG_COLOR)

# Создаем игровое поле
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=symbol_font, width=2, height=1,
                        command=lambda r=i, c=j: on_click(r, c),
                        bg=BUTTON_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                        relief="ridge", borderwidth=2)
        btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        row.append(btn)
    buttons.append(row)

# Настройка веса строк и столбцов
for i in range(3):
    game_frame.grid_rowconfigure(i, weight=1)
    game_frame.grid_columnconfigure(i, weight=1)

# Кнопка сброса
reset_btn = tk.Button(game_frame, text="Новая игра", font=button_font,
                      command=reset_game, bg=RESET_COLOR, fg=TEXT_COLOR,
                      activebackground=BUTTON_ACTIVE_COLOR)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

window.mainloop()
