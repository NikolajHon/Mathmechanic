import tkinter as tk
from tkinter import ttk
from typing import Optional
from field import Field


class SolverUI:
    def __init__(self, root: Optional[tk.Tk], field: Field, solve_callback: Optional[callable]):
        self.root = root or tk.Tk()
        self.field = field
        self.solve_callback = solve_callback
        self.row_labels = []
        self.col_labels = []
        self.buttons = [[None for _ in range(field.cols)] for _ in range(field.rows)]

        self._create_ui()
        self.root.after(2000, self.solve_callback)

    def _create_ui(self):
        for r in range(self.field.rows):
            for c in range(self.field.cols):
                value = self.field.initial_state[r][c]

                bg_color = "white" if self.field.active_cells[r][c] else "lightgrey"
                fg_color = "black" if self.field.active_cells[r][c] else "darkgrey"

                button = tk.Button(
                    self.root,
                    text=str(value),
                    bg=bg_color,
                    fg=fg_color,
                    width=5,
                    borderwidth=1,
                    relief="solid",
                    state="disabled"
                )
                button.grid(row=r + 1, column=c + 1, padx=2, pady=2)
                self.buttons[r][c] = button

        for r in range(self.field.rows):
            row_sum = self._calculate_row_sum(r)
            row_label = ttk.Label(self.root, text=f"{row_sum}/{self.field.row_targets[r]}", width=5, borderwidth=1,
                                  relief="solid")
            row_label.grid(row=r + 1, column=0, padx=2, pady=2)
            self.row_labels.append(row_label)

        for c in range(self.field.cols):
            col_sum = self._calculate_col_sum(c)
            col_label = ttk.Label(self.root, text=f"{col_sum}/{self.field.column_targets[c]}", width=5, borderwidth=1,
                                  relief="solid")
            col_label.grid(row=0, column=c + 1, padx=2, pady=2)
            self.col_labels.append(col_label)

        solve_button = ttk.Button(self.root, text="Solve", command=self.solve_callback)
        solve_button.grid(row=self.field.rows + 1, column=0, columnspan=self.field.cols + 1, pady=10)

    def update_ui(self, active_cells):
        for r in range(self.field.rows):
            for c in range(self.field.cols):
                value = self.field.initial_state[r][c]

                bg_color = "white" if active_cells[r][c] else "lightgrey"
                fg_color = "black" if active_cells[r][c] else "darkgrey"

                self.buttons[r][c].config(text=str(value), bg=bg_color, fg=fg_color)

    def finish(self, active_cells):
        self.update_ui(active_cells)

    def update_sums(self, active_cells):
        for r in range(self.field.rows):
            row_sum = self._calculate_row_sum(r, active_cells)
            self.row_labels[r].config(text=f"{row_sum}/{self.field.row_targets[r]}")
        for c in range(self.field.cols):
            col_sum = self._calculate_col_sum(c, active_cells)
            self.col_labels[c].config(text=f"{col_sum}/{self.field.column_targets[c]}")

    def display_message(self, message: str):
        message_label = ttk.Label(self.root, text=message, font=("Arial", 14))
        message_label.grid(row=self.field.rows + 2, column=0, columnspan=self.field.cols + 1, pady=10)

    def _calculate_row_sum(self, row, active_cells=None):
        active_cells = active_cells or self.field.active_cells
        return sum(self.field.initial_state[row][c] for c in range(self.field.cols) if active_cells[row][c])

    def _calculate_col_sum(self, col, active_cells=None):
        active_cells = active_cells or self.field.active_cells
        return sum(self.field.initial_state[r][col] for r in range(self.field.rows) if active_cells[r][col])

    def start(self):
        self.root.mainloop()
