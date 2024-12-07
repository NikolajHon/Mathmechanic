import time
from typing import List, Dict, Tuple
from field import Field
from solvers.Solver import Solver


class ForwardCheckingSolver(Solver):
    def __init__(self, field: Field, algorithm_name: str) -> None:
        super().__init__(field, algorithm_name)
        self.domains: Dict[Tuple[int, int], List[bool]] = {}

    def solve(self) -> None:
        start_time: float = time.time()
        self.solution: List[List[bool]] = None
        self.iteration_count: int = 0

        for r in range(self.field.rows):
            for c in range(self.field.cols):
                self.domains[(r, c)] = [True, False]

        if self.forward_check(0, {}):
            self.finalize_solution(start_time)
            time.sleep(500)
        else:
            self.ui.display_message(f"No valid solution found after {self.iteration_count} iterations.")
            self.ui.root.after(2000, self.ui.root.destroy)

    def forward_check(self, variable_index: int, assignment: Dict[Tuple[int, int], bool]) -> bool:
        if len(assignment) == self.field.rows * self.field.cols:
            active_cells = [[False for _ in range(self.field.cols)] for _ in range(self.field.rows)]
            for (r, c), value in assignment.items():
                active_cells[r][c] = value
            if self.is_valid_solution(active_cells):
                self.solution = active_cells
                return True
            return False

        variables = list(self.domains.keys())
        var = variables[variable_index]

        for value in self.domains[var][:]:
            if self.is_consistent(var, value, assignment):
                self.iteration_count += 1

                assignment[var] = value
                saved_domains = {v: self.domains[v][:] for v in self.domains}

                if self.forward_check_domains(var, value, assignment):
                    active_cells = [[False for _ in range(self.field.cols)] for _ in range(self.field.rows)]
                    for (r, c), val in assignment.items():
                        active_cells[r][c] = val
                    self.ui.update_ui(active_cells)
                    self.ui.update_sums(active_cells)
                    self.ui.root.update_idletasks()
                    self.ui.root.update()

                    if self.forward_check(variable_index + 1, assignment):
                        return True

                self.domains = saved_domains
                del assignment[var]

        return False

    def is_consistent(self, var: Tuple[int, int], value: bool, assignment: Dict[Tuple[int, int], bool]) -> bool:
        r, c = var
        cell_value = self.field.initial_state[r][c] if value else 0

        row_sum = sum(
            self.field.initial_state[r][col] if assignment.get((r, col), False) else 0
            for col in range(self.field.cols)
        )
        col_sum = sum(
            self.field.initial_state[row][c] if assignment.get((row, c), False) else 0
            for row in range(self.field.rows)
        )

        row_sum += cell_value - (self.field.initial_state[r][c] if assignment.get((r, c), False) else 0)
        col_sum += cell_value - (self.field.initial_state[r][c] if assignment.get((r, c), False) else 0)

        if row_sum > self.field.row_targets[r] or col_sum > self.field.column_targets[c]:
            return False

        if all((r, col) in assignment for col in range(self.field.cols)) and row_sum != self.field.row_targets[r]:
            return False
        if all((row, c) in assignment for row in range(self.field.rows)) and col_sum != self.field.column_targets[c]:
            return False

        return True

    def forward_check_domains(self, var: Tuple[int, int], value: bool, assignment: Dict[Tuple[int, int], bool]) -> bool:


        for v in self.domains:
            if v not in assignment:
                new_domain = []
                for val in self.domains[v]:
                    temp_assignment = assignment.copy()
                    temp_assignment[v] = val
                    if self.is_consistent(v, val, temp_assignment):
                        new_domain.append(val)
                if not new_domain:
                    return False
                self.domains[v] = new_domain
        return True
