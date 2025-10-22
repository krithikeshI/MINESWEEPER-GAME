import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.buttons = []
        self.generate_mines()
        self.calculate_numbers()
        self.create_gui()

    def generate_mines(self):
        mine_positions = random.sample(range(self.rows * self.cols), self.mines)
        for position in mine_positions:
            row, col = divmod(position, self.cols)
            self.board[row][col] = "M"

    def calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != "M":
                    for i in range(max(0, row - 1), min(self.rows, row + 2)):
                        for j in range(max(0, col - 1), min(self.cols, col + 2)):
                            if self.board[i][j] == "M":
                                self.board[row][col] += 1

    def create_gui(self):
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, text=" ", width=3, height=1, command=lambda r=row, c=col: self.reveal_cell(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def reveal_cell(self, row, col):
        if not self.revealed[row][col]:
            self.revealed[row][col] = True
            button = self.buttons[row][col]
            button.config(text=str(self.board[row][col]))

            if self.board[row][col] == 0:
                for i in range(max(0, row - 1), min(self.rows, row + 2)):
                    for j in range(max(0, col - 1), min(self.cols, col + 2)):
                        if not self.revealed[i][j]:
                            self.reveal_cell(i, j)

            if self.board[row][col] == "M":
                self.game_over()
            else:
                self.check_win()

    def game_over(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.revealed[row][col] = True
                button = self.buttons[row][col]
                if self.board[row][col] == "M":
                    button.config(text="💣", state=tk.DISABLED, disabledforeground="red")
                else:
                    button.config(state=tk.DISABLED, disabledforeground="black")

        messagebox.showinfo("Game Over", "Oops! You hit a mine. Game over!")

    def check_win(self):
        unrevealed_count = sum(row.count(False) for row in self.revealed)
        if unrevealed_count == self.mines:
            messagebox.showinfo("Congratulations", "Congratulations! You won.")

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    minesweeper_game = Minesweeper(root, rows=10, cols=10, mines=20)
    root.mainloop()

if __name__ == "__main__":
    main()
