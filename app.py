import tkinter as tk
from tkinter import ttk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)
        self.master.configure(bg='#121212')

        # Create a canvas for the game with a gradient background
        self.canvas = tk.Canvas(master, width=400, height=400, bg="#2e2e2e", highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(master, bg='#121212')
        self.button_frame.pack(pady=20)

        # Create stylish buttons with rounded corners and shadow effects
        self.style = ttk.Style()
        self.style.configure("TButton",
                             padding=10,
                             relief="flat",
                             background="#007bff",
                             foreground="black",
                             font=("Helvetica", 14, "bold"),
                             borderwidth=0,
                             focuscolor="none")

        self.style.map("TButton",
                       background=[("active", "#0056b3"), ("!disabled", "#007bff")],
                       foreground=[("active", "black"), ("!disabled", "black")],
                       relief=[("active", "groove"), ("!disabled", "flat")])

        self.restart_button = ttk.Button(self.button_frame, text="Play Again", command=self.restart_game, style="TButton")
        self.quit_button = ttk.Button(self.button_frame, text="Quit", command=master.quit, style="TButton")

        # Add hover effects
        self.restart_button.bind("<Enter>", lambda e: self.restart_button.configure(style="Hover.TButton"))
        self.restart_button.bind("<Leave>", lambda e: self.restart_button.configure(style="TButton"))
        self.quit_button.bind("<Enter>", lambda e: self.quit_button.configure(style="Hover.TButton"))
        self.quit_button.bind("<Leave>", lambda e: self.quit_button.configure(style="TButton"))

        # Create a style for the hover state
        self.style.configure("Hover.TButton",
                             background="#0056b3",
                             foreground="white")

        # Game initialization
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.food = self.create_food()
        self.game_over = False
        self.score = 0

        # Bind keyboard events
        self.master.bind("<KeyPress>", self.change_direction)
        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.snake_direction = event.keysym

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == "Up":
            new_head = (head_x, head_y - 20)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + 20)
        elif self.snake_direction == "Left":
            new_head = (head_x - 20, head_y)
        elif self.snake_direction == "Right":
            new_head = (head_x + 20, head_y)

        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.create_food()
            self.score += 10

        if (new_head[0] < 0 or new_head[0] >= 400 or new_head[1] < 0 or new_head[1] >= 400
                or new_head in self.snake[1:]):
            self.game_over = True

    def draw(self):
        self.canvas.delete(tk.ALL)

        # Draw gradient background
        self.draw_gradient()

        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="#28a745", outline="black", width=2)
        food_x, food_y = self.food
        self.canvas.create_rectangle(food_x, food_y, food_x + 20, food_y + 20, fill="#dc3545", outline="black", width=2)

        if self.game_over:
            self.canvas.create_text(200, 150, text=f"GAME OVER\nScore: {self.score}", fill="white", font=("Helvetica", 24, "bold"))
            self.restart_button.pack(side=tk.LEFT, padx=10)
            self.quit_button.pack(side=tk.RIGHT, padx=10)

    def draw_gradient(self):
        for i in range(400):
            color = self._rgb((int(46 + (i * (60 - 46) / 400)), int(46 + (i * (60 - 46) / 400)), int(46 + (i * (60 - 46) / 400))))
            self.canvas.create_line(0, i, 400, i, fill=color)

    def _rgb(self, rgb):
        return "#%02x%02x%02x" % rgb

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw()
            self.master.after(100, self.update)

    def restart_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.food = self.create_food()
        self.game_over = False
        self.score = 0
        self.restart_button.pack_forget()
        self.quit_button.pack_forget()
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
