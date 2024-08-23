import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root, level=1):
        self.root = root
        self.level = level
        self.size = 2 + level  # Level 1: 3x3 grid, Level 2: 4x4, ..., Level 5: 7x7
        self.mines = level  # Level 1: 1 mine, Level 2: 2 mines, ..., Level 5: 5 mines
        self.mines_remaining = self.mines
        self.buttons = {}
        self.mines_locations = []
        self.colors = {
            1: 'blue', 2: 'green', 3: 'red', 4: 'purple', 5: 'brown',
            6: 'cyan', 7: 'black', 8: 'gray'
        }
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg='#F0F8FF')  # Alice Blue background for a light, clean look
        self.root.title(f'Minesweeper - Level {self.level}')
        self.root.geometry(f'{self.size * 80}x{self.size * 80 + 70}')
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text=f'Mines: {self.mines_remaining}', 
                                   font=('Arial', 20), bg='#F0F8FF', anchor='w')
        self.status_bar.pack(fill=tk.X)

        # Game Board
        board_frame = tk.Frame(self.root, bg='#A9A9A9', padx=10, pady=10)
        board_frame.pack()

        for row in range(self.size):
            for col in range(self.size):
                btn = tk.Button(board_frame, width=5, height=2, font=('Arial', 14, 'bold'), 
                                bg='#F0F0F0', anchor='center', command=lambda r=row, c=col: self.on_click(r, c))
                btn.bind("<Button-3>", lambda e, r=row, c=col: self.on_right_click(r, c))
                btn.grid(row=row, column=col, padx=3, pady=3)
                self.buttons[(row, col)] = btn

        self.place_mines()

    def place_mines(self):
        mines = self.mines
        while mines > 0:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if (row, col) not in self.mines_locations:
                self.mines_locations.append((row, col))
                mines -= 1

    def on_click(self, row, col):
        if (row, col) in self.mines_locations:
            self.game_over()
        else:
            self.reveal(row, col)
            if self.check_win():
                self.win_game()

    def on_right_click(self, row, col):
        btn = self.buttons[(row, col)]
        if btn["text"] == "":
            btn.config(text="🚩", fg="red", bg='#FFFACD')  # Light Yellow when flagged
            self.mines_remaining -= 1
        elif btn["text"] == "🚩":
            btn.config(text="", bg='#ADD8E6')  # Reset to Light Blue when unflagged
            self.mines_remaining += 1
        self.update_status()

    def reveal(self, row, col):
        if self.buttons[(row, col)]["state"] == "disabled":
            return

        self.buttons[(row, col)].config(state="disabled", relief=tk.SUNKEN, bg='#E0FFFF')  # Light Cyan for revealed cells
        mines_around = self.count_mines_around(row, col)

        if mines_around == 0:
            for r in range(max(0, row - 1), min(self.size, row + 2)):
                for c in range(max(0, col - 1), min(self.size, col + 2)):
                    if (r, c) != (row, col):
                        self.reveal(r, c)
        else:
            self.buttons[(row, col)].config(text=str(mines_around), fg=self.colors[mines_around], bg='#E6E6FA')  # Lavender for numbers

    def count_mines_around(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.size, row + 2)):
            for c in range(max(0, col - 1), min(self.size, col + 2)):
                if (r, c) in self.mines_locations:
                    count += 1
        return count

    def check_win(self):
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.mines_locations and self.buttons[(row, col)]["state"] != "disabled":
                    return False
        return True

    def game_over(self):
        for row, col in self.mines_locations:
            self.buttons[(row, col)].config(text="💣", fg="white", bg="red")  # Red background for mines when game over
        messagebox.showinfo("Game Over", "You hit a mine! Game over!")
        self.root.destroy()

    def win_game(self):
        if self.level < 5:
            next_level = self.level + 1
            messagebox.showinfo("Level Complete!", f"Congratulations! Moving to Level {next_level}.")
            self.root.destroy()
            new_root = tk.Tk()
            game = Minesweeper(new_root, level=next_level)
            new_root.mainloop()
        else:
            messagebox.showinfo("Congratulations", "You completed all levels!")
            self.root.destroy()

    def update_status(self):
        self.status_bar.config(text=f'Mines Remaining: {self.mines_remaining}')

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
