import tkinter as tk
from tkinter import ttk


def main():
    window = tk.Tk()
    window.title("Peg Solitaire")
    window.resizable(False, False)

    frame = ttk.Frame(window, padding=20)
    frame.pack()

    ttk.Label(frame, text="Peg Solitaire", font=("Arial", 18)).pack(pady=5)

    # A canvas lets us draw lines using start and end coordinates.
    canvas = tk.Canvas(frame, width=280, height=45, highlightthickness=0)
    canvas.pack(pady=10)
    canvas.create_line(10, 10, 270, 10, width=2)
    canvas.create_line(10, 30, 270, 30, fill="blue", width=2)

    show_hints = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, text="Show hints", variable=show_hints).pack(anchor="w")

    ttk.Label(frame, text="Choose a board type:").pack(anchor="w", pady=(15, 5))
    board_type = tk.StringVar(value="English")
    for name in ("English", "Hexagon", "Diamond"):
        ttk.Radiobutton(
            frame, text=name, variable=board_type, value=name
        ).pack(anchor="w", pady=2)

    ttk.Button(frame, text="Close", command=window.destroy).pack(pady=(15, 0))
    window.mainloop()


if __name__ == "__main__":
    main()
