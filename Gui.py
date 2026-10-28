import math
import tkinter as tk
from tkinter import ttk

from game import PegSolitaireGame


class PegSolitaireGUI:

    def __init__(self, window):
        self.window = window
        self.window.title("Peg Solitaire")
        self.window.resizable(False, False)

        self.game = PegSolitaireGame()
        self.selected = None
        self.message = "Select a peg, then an empty hole."
        self.game_over = False
        self.show_lines = tk.BooleanVar(value=False)
        self.board_type = tk.StringVar(value="English")
        self.board_size = tk.StringVar(value="7")
        self.board_info = tk.StringVar()
        self.status = tk.StringVar()

        frame = ttk.Frame(window, padding=20)
        frame.pack()

        # Display the title of the game.
        ttk.Label(
            frame,
            text="Peg Solitaire",
            font=("Arial", 18),
        ).pack(pady=5)

        # Display the board type and size.
        ttk.Label(
            frame,
            textvariable=self.board_info,
        ).pack(pady=5)

        self.canvas = tk.Canvas(
            frame,
            width=350,
            height=350,
            background="#eee8dc",
            highlightthickness=0,
        )
        self.canvas.pack(pady=10)

        # Display the option to show guide lines.
        ttk.Checkbutton(
            frame,
            text="Show guide lines",
            variable=self.show_lines,
            command=self.draw_board,
        ).pack(anchor="w")

        # Display the board type selection.
        ttk.Label(
            frame,
            text="Board type:",
        ).pack(anchor="w", pady=(15, 5))

        for name in ("English", "Hexagon", "Diamond"):
            ttk.Radiobutton(
                frame,
                text=name,
                variable=self.board_type,
                value=name,
            ).pack(anchor="w", pady=2)

        ttk.Label(frame, text="Board size:").pack(anchor="w", pady=(10, 5))
        ttk.Combobox(
            frame, textvariable=self.board_size, values=("7", "9", "11"),
            state="readonly", width=10,
        ).pack(anchor="w")

        # Settings are pending until New Game is clicked.
        ttk.Label(
            frame,
            text="Choose settings, then click New Game.",
        ).pack(pady=10)

        # Display the game status.
        ttk.Label(
            frame,
            textvariable=self.status,
        ).pack(pady=5)

        # Display the "New Game" button.
        ttk.Button(
            frame,
            text="New Game",
            command=self.new_game,
        ).pack(fill="x", pady=5)

        # Display the "Close" button.
        ttk.Button(
            frame,
            text="Close",
            command=self.window.destroy,
        ).pack(fill="x", pady=5)

        self.draw_board()

    def new_game(self):
        self.game = PegSolitaireGame(
            board_type=self.board_type.get(), size=int(self.board_size.get())
        )
        self.selected = None
        self.message = "Select a peg, then an empty hole."
        self.game_over = False
        self.draw_board()

    def draw_board(self):
        """Scale and center the active layout, then draw guides and holes."""
        self.canvas.delete("all")
        center = self.game.SIZE // 2
        points = {}
        for row in range(self.game.SIZE):
            for col in range(self.game.SIZE):
                if not self.game.is_playable(row, col):
                    continue
                q, r = col - center, row - center
                if self.game.board_type == "Hexagon":
                    points[(row, col)] = (q + r / 2, r * math.sqrt(3) / 2)
                else:
                    points[(row, col)] = (q, r)

        width = float(self.canvas.cget("width"))
        height = float(self.canvas.cget("height"))
        min_x = min(x for x, y in points.values())
        max_x = max(x for x, y in points.values())
        min_y = min(y for x, y in points.values())
        max_y = max(y for x, y in points.values())
        scale = min((width - 60) / (max_x - min_x),
                    (height - 60) / (max_y - min_y))
        radius = min(17, scale * 0.34)
        positions = {
            cell: (width / 2 + (x - (min_x + max_x) / 2) * scale,
                   height / 2 + (y - (min_y + max_y) / 2) * scale)
            for cell, (x, y) in points.items()
        }

        if self.show_lines.get():
            # Draw each undirected edge once using the model's allowed axes.
            for (row, col), position in positions.items():
                for dr, dc in self.game.directions:
                    neighbor = (row + dr, col + dc)
                    if neighbor in positions and (row, col) < neighbor:
                        self.canvas.create_line(
                            *position, *positions[neighbor],
                            fill="#aaa08c", width=2,
                        )

        for (row, col), (x, y) in positions.items():
            hole = self.game.board[row][col]
            color = "#28776b" if hole == self.game.PEG else "#ffffff"
            if (row, col) == self.selected:
                color = "#e5aa32"
            item = self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=color, outline="#555555", width=2,
            )
            self.canvas.tag_bind(
                item, "<Button-1>",
                lambda event, row=row, col=col: self.on_hole_click(row, col),
            )

        self.board_info.set(f"{self.game.board_type} board - Size {self.game.SIZE}")
        self.status.set(
            f"Pegs remaining: {self.game.count_pegs()} | {self.message}"
        )

    # Handle user clicks on holes in the board.
    def on_hole_click(self, row, col):
        if not self.game.is_playable(row, col) or self.game_over:
            return

        cell = (row, col)
        if self.game.board[row][col] == self.game.PEG:
            if self.selected == cell:
                self.selected = None
                self.message = "Selection cleared. Select a peg."
            else:
                self.selected = cell
                self.message = "Peg selected. Click an empty hole to jump."
        elif self.selected is None:
            self.message = "Select a filled peg before clicking an empty hole."
        elif self.game.make_move(self.selected, cell):
            self.selected = None
            self.game_over = self.game.is_game_over()
            if self.game_over:
                if self.game.count_pegs() == 1:
                    self.message = "You win! One peg remains."
                else:
                    self.message = "Game over: no valid moves remain."
            else:
                self.message = "Move made. Select another peg."
        else:
            self.message = "Invalid move. Jump over a peg into an empty hole."

        self.draw_board()


def main():
    window = tk.Tk()
    PegSolitaireGUI(window)
    window.mainloop()


if __name__ == "__main__":
    main()