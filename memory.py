import tkinter as tk
from tkinter import messagebox
import random
import time

class NeonMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry("400x500")
        self.root.configure(bg='#121212')

        title_frame = tk.Frame(root, bg='#121212')
        title_frame.pack(pady=10)

        title_label = tk.Label(title_frame, text="Memory Game", font=("Helvetica", 16, "bold"), fg='#7FFF00', bg='#121212')
        title_label.pack(side=tk.LEFT)

        self.score = 0
        self.lives = 3
        self.highest_score = 0
        self.level = 1

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Helvetica", 12), fg='#7FFF00', bg='#121212')
        self.score_label.pack(anchor=tk.W)

        self.lives_label = tk.Label(root, text=f"Lives: ❤️❤️❤️", font=("Helvetica", 12), fg='#7FFF00', bg='#121212')
        self.lives_label.pack(anchor=tk.W)

        self.highest_score_label = tk.Label(root, text=f"Highest Score: {self.highest_score}", font=("Helvetica", 12), fg='#7FFF00', bg='#121212')
        self.highest_score_label.pack(anchor=tk.W)

        self.level_label = tk.Label(root, text=f"Level: {self.level}", font=("Helvetica", 12), fg='#7FFF00', bg='#121212')
        self.level_label.pack(anchor=tk.W)

        game_frame = tk.Frame(root, bg='#121212')
        game_frame.pack()

        self.squares = []
        self.sequence = []
        self.player_sequence = []
        self.speed = 800

        for i in range(4):
            for j in range(4):
                square = tk.Button(game_frame, text='■', width=4, height=2, font=("Helvetica", 12),
                                   command=lambda idx=(i * 4 + j): self.handle_square_click(idx), bg='#1E1E1E', fg='#7FFF00', relief=tk.FLAT, bd=3, padx=10, pady=10, borderwidth=0, highlightthickness=0, activebackground='#121212')
                square.grid(row=i, column=j, padx=5, pady=5)
                square.bind("<Enter>", lambda event, btn=square: self.on_enter(event, btn))
                square.bind("<Leave>", lambda event, btn=square: self.on_leave(event, btn))
                self.squares.append(square)

        reset_button = tk.Button(root, text="Reset Game", font=("Helvetica", 12), command=self.start_game, bg='#1E1E1E', fg='#7FFF00', relief=tk.FLAT, bd=3, padx=10, pady=5, activebackground='#121212', cursor="hand2")
        reset_button.pack(pady=10)
        reset_button.bind("<Enter>", lambda event, btn=reset_button: self.on_enter(event, btn))
        reset_button.bind("<Leave>", lambda event, btn=reset_button: self.on_leave(event, btn))

        self.start_game()

    def start_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.update_score()
        self.update_lives()
        self.update_level()

        self.sequence = []
        self.player_sequence = []
        self.speed = 800

        self.generate_sequence()
        self.show_sequence()

    def handle_square_click(self, index):
        self.player_sequence.append(index)
        self.squares[index].config(bg='#7FFF00')

        self.root.after(500, lambda: self.reset_square_color(index))

        if len(self.player_sequence) == len(self.sequence):
            if self.player_sequence == self.sequence:
                self.score += 1
                self.update_score()

                if self.score > self.highest_score:
                    self.highest_score = self.score
                    self.update_highest_score()

                if self.score % 5 == 0:
                    self.lives += 1
                    self.update_lives()

                if self.score % 10 == 0:
                    self.level += 1
                    self.speed -= 50
                    self.update_level()

                self.player_sequence = []
                self.root.after(1200, self.start_round)
            else:
                self.lives -= 1
                self.update_lives()

                if self.lives == 0:
                    messagebox.showinfo("Game Over", f"Your Score: {self.score}\nTry again.")
                    self.start_game()

    def reset_square_color(self, index):
        self.squares[index].config(bg='#1E1E1E')

    def start_round(self):
        self.generate_sequence()
        self.show_sequence()

    def generate_sequence(self):
        self.sequence = random.sample(range(16), self.level * 2)

    def show_sequence(self):
        for index in self.sequence:
            self.highlight_square(index)
            self.root.update()
            time.sleep(self.speed / 2000)
            self.reset_square_color(index)
            self.root.update()
            time.sleep(self.speed / 2000)

    def highlight_square(self, index):
        self.squares[index].config(bg='#7FFF00')
        self.root.update()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_lives(self):
        hearts = "❤️" * self.lives
        self.lives_label.config(text=f"Lives: {hearts}")

    def update_highest_score(self):
        self.highest_score_label.config(text=f"Highest Score: {self.highest_score}")

    def update_level(self):
        self.level_label.config(text=f"Level: {self.level}")

    def on_enter(self, event, btn):
        btn.config(bg='#303030', relief=tk.SUNKEN)

    def on_leave(self, event, btn):
        btn.config(bg='#1E1E1E', relief=tk.FLAT)

root = tk.Tk()
root.title("Neon Memory Game")
root.geometry("400x500")
root.configure(bg='#121212')

neon_game = NeonMemoryGame(root)

root.mainloop()
