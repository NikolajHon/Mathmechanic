import time
from typing import List
from field import Field
from solvers.Solver import Solver


class BacktrackingSolver(Solver):
    def __init__(self, field: Field, algorithm_name: str) -> None:
        super().__init__(field, algorithm_name)
        self.active_cells: List[List[bool]] = [[False for _ in range(self.field.cols)] for _ in range(self.field.rows)]
        self.found_solution: bool = False

    def toggle_cell(self, r: int, c: int) -> None:
        self.active_cells[r][c] = not self.active_cells[r][c]
        self.ui.update_ui(self.active_cells)
        self.ui.update_sums(self.active_cells)

    def solve(self) -> None:
        start_time: float = time.time()
        self.solution: List[List[bool]] = None
        self.iteration_count: int = 0
        self.found_solution = False

        self.backtrack(0, 0)

        self.finalize_solution(start_time)

    def backtrack(self, row: int, col: int) -> None:
        if self.found_solution:
            return

        self.iteration_count += 1

        self.ui.update_ui(self.active_cells)
        self.ui.update_sums(self.active_cells)
        self.ui.root.update_idletasks()
        self.ui.root.update()

        if row == self.field.rows:
            if self.is_valid_solution(self.active_cells):
                self.solution = [row[:] for row in self.active_cells]
                self.found_solution = True
            return

        if not self.can_continue():
            return

        next_row, next_col = (row, col + 1) if col + 1 < self.field.cols else (row + 1, 0)

        self.active_cells[row][col] = True
        self.backtrack(next_row, next_col)

        if self.found_solution:
            return

        self.active_cells[row][col] = False
        self.backtrack(next_row, next_col)

    def can_continue(self) -> bool:
        for r in range(self.field.rows):
            if self.field.calculate_row_sum(r, self.active_cells) > self.field.row_targets[r]:
                return False
        for c in range(self.field.cols):
            if self.field.calculate_column_sum(c, self.active_cells) > self.field.column_targets[c]:
                return False
        return True
