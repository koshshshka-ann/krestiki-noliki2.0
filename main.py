import tkinter as tk
from tkinter import messagebox
import random

# Настройки игры
DEFAULT_PLAYER_SYMBOL = "X"

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("300x400")

# Переменные игры
current_player = DEFAULT_PLAYER_SYMBOL  # Объявляем глобальную переменную в начале
player_symbol = DEFAULT_PLAYER_SYMBOL
computer_symbol = "O"
buttons = []
game_active = False

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
    game_frame.pack()


def reset_game():
    global current_player, game_active
    current_player = "X"
    game_active = True
    for row in buttons:
        for button in row:
            button.config(text="")
    game_frame.pack_forget()
    symbol_frame.pack()


def check_winner():
    # Проверка строк и столбцов
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return True
    # Проверка диагоналей
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True
    return False


def is_draw():
    return all(button["text"] != "" for row in buttons for button in row)


def end_game(message):
    global game_active
    game_active = False
    messagebox.showinfo("Игра окончена", message)


def computer_move():
    global current_player  # Перенесли объявление в начало функции

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

    if check_winner():
        end_game(f"Игрок ({player_symbol}) победил!")
    elif is_draw():
        end_game("Ничья!")
    else:
        current_player = computer_symbol
        # Задержка перед ходом компьютера для удобства восприятия
        window.after(500, computer_move)


# Фрейм для выбора символа
symbol_frame = tk.Frame(window)
tk.Label(symbol_frame, text="Выберите, чем будете играть:", font=("Arial", 14)).pack(pady=10)
tk.Button(symbol_frame, text="Крестики (X)", font=("Arial", 12), width=15,
          command=lambda: choose_symbol("X")).pack(pady=5)
tk.Button(symbol_frame, text="Нолики (O)", font=("Arial", 12), width=15,
          command=lambda: choose_symbol("O")).pack(pady=5)
symbol_frame.pack()

# Фрейм для игрового поля
game_frame = tk.Frame(window)

# Создаем игровое поле
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(game_frame, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

# Кнопка сброса
reset_btn = tk.Button(game_frame, text="Новая игра", command=reset_game)
reset_btn.grid(row=3, column=0, columnspan=3, sticky="we", padx=10, pady=10)

window.mainloop()
