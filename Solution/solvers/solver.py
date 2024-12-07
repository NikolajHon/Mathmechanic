import time
import tkinter as tk
from typing import List, Optional
from ui import SolverUI
from field import Field


class Solver:
    def __init__(self, field: Field, algorithm_name: str , parent: Optional[tk.Tk] = None, ) -> None:
        self.field: Field = field
        self.algorithm_name: str = algorithm_name
        self.solution: Optional[List[List[bool]]] = None
        self.iteration_count: int = 0
        self.solution_found: bool = False

        self.ui: SolverUI = SolverUI(root=parent, field=self.field, solve_callback=self.solve)

    def toggle_cell(self, r: int, c: int) -> None:
        self.field.active_cells[r][c] = not self.field.active_cells[r][c]
        self.ui.update_ui(self.field.active_cells)
        self.ui.update_sums(self.field.active_cells)

    def finalize_solution(self, start_time: float) -> None:
        elapsed_time: float = time.time() - start_time
        result_message: str

        if self.solution:
            self.field.active_cells = [row[:] for row in self.solution]
            self.ui.finish(self.field.active_cells)
            result_message = (
                f"Solution found!\nTime taken: {elapsed_time:.2f} seconds\nIterations: {self.iteration_count}"
            )
        else:
            result_message = "No valid solution could be found."

        self.write_statistics_to_file(elapsed_time, result_message)

        self.ui.display_message(result_message)
        self.ui.root.after(2000, self.ui.root.destroy)

    def is_valid_solution(self, active_cells: List[List[bool]]) -> bool:
        for r in range(self.field.rows):
            if self.field.calculate_row_sum(r, active_cells) > self.field.row_targets[r]:
                return False
        for c in range(self.field.cols):
            if self.field.calculate_column_sum(c, active_cells) > self.field.column_targets[c]:
                return False

        for r in range(self.field.rows):
            if self.field.calculate_row_sum(r, active_cells) != self.field.row_targets[r]:
                return False
        for c in range(self.field.cols):
            if self.field.calculate_column_sum(c, active_cells) != self.field.column_targets[c]:
                return False
        return True

    def write_statistics_to_file(self, elapsed_time: float, result_message: str) -> None:
        with open("solver_statistics.txt", "a") as file:
            file.write(f"Algorithm: {self.algorithm_name}\n")
            file.write("Solver Run:\n")
            file.write(f"Time taken: {elapsed_time:.2f} seconds\n")
            file.write(f"Iterations: {self.iteration_count}\n")
            file.write(f"Result: {result_message}\n")
            file.write(f"Field Dimensions: {self.field.rows}x{self.field.cols}\n")
            file.write("Row Targets: " + ", ".join(map(str, self.field.row_targets)) + "\n")
            file.write("Column Targets: " + ", ".join(map(str, self.field.column_targets)) + "\n")
            file.write("Initial State:\n")
            for row in self.field.initial_state:
                file.write(" ".join(map(str, row)) + "\n")
            file.write("-" * 40 + "\n")

    def start(self) -> None:
        self.ui.start()
