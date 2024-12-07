from typing import List


class Field:
    def __init__(self, row_targets, column_targets, initial_state):
        self.row_targets = row_targets
        self.column_targets = column_targets
        self.initial_state = initial_state
        self.rows = len(initial_state)
        self.cols = len(initial_state[0])
        self.active_cells = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.row_remaining = row_targets[:]
        self.col_remaining = column_targets[:]

    def copy(self):
        return Field(self.row_targets, self.column_targets, self.initial_state)

    def calculate_sum_diff(self, active_cells: List[List[bool]]) -> float:
        sum_diff: float = 0
        for r in range(self.rows):
            sum_diff += abs(self.calculate_row_sum(r, active_cells) - self.row_targets[r])
        for c in range(self.cols):
            sum_diff += abs(self.calculate_column_sum(c, active_cells) - self.column_targets[c])
        return sum_diff

    def calculate_row_sum(self, row: int, active_cells: List[List[bool]]) -> int:
        return sum(self.initial_state[row][c] for c in range(self.cols) if active_cells[row][c])

    def calculate_column_sum(self, col: int, active_cells: List[List[bool]]) -> int:
        return sum(self.initial_state[r][col] for r in range(self.rows) if active_cells[r][col])
