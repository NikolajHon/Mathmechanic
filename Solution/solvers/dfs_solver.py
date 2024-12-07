import time
from typing import List
from field import Field
from solvers.Solver import Solver


class DfsSolver(Solver):
    def __init__(self, field: Field,algorithm_name: str ) -> None:
        super().__init__(field, algorithm_name)
        self.active_cells: List[List[bool]] = [[True for _ in range(self.field.cols)] for _ in range(self.field.rows)]

    def toggle_cell(self, r: int, c: int) -> None:
        self.active_cells[r][c] = not self.active_cells[r][c]
        self.ui.update_ui(self.active_cells)
        self.ui.update_sums(self.active_cells)

    def solve(self) -> None:
        start_time: float = time.time()
        self.solution_found: bool = False
        self.solution: List[List[bool]] = None
        self.iteration_count: int = 0

        self.dfs(0, 0, [row[:] for row in self.active_cells])

        self.finalize_solution(start_time)

    def dfs(self, row: int, col: int, active_cells: List[List[bool]]) -> None:
        stack: List[tuple[int, int, List[List[bool]]]] = [(row, col, [row[:] for row in active_cells])]

        while stack and not self.solution_found:
            self.iteration_count += 1

            current_row, current_col, current_active_cells = stack.pop()

            if current_row == self.field.rows:
                if self.is_valid_solution(current_active_cells):
                    self.solution = [row[:] for row in current_active_cells]
                    self.solution_found = True
                continue

            next_row: int
            next_col: int
            next_row, next_col = (current_row, current_col + 1) if current_col + 1 < self.field.cols else (current_row + 1, 0)

            stack.append((next_row, next_col, [row[:] for row in current_active_cells]))
            current_active_cells[current_row][current_col] = False

            self.ui.update_ui(current_active_cells)
            self.ui.update_sums(current_active_cells)
            self.ui.root.update_idletasks()
            self.ui.root.update()

            if not self.solution_found:
                stack.append((next_row, next_col, [row[:] for row in current_active_cells]))
