import time
import json
from tkinter.constants import FIRST

from field import Field
from solvers.dfs_solver import DfsSolver
from solvers.backtracking_solver import BacktrackingSolver
from solvers.forward_check_solver import ForwardCheckingSolver

if __name__ == "__main__":
    with open("maps.json", "r") as f:
        data = json.load(f)
    open("solver_statistics.txt", "w")
    for i, map_data in enumerate(data["maps"]):
        row_targets = map_data["row_targets"]
        column_targets = map_data["column_targets"]
        initial_state = map_data["initial_state"]

        print(f"Processing map {i + 1}...")

        field = Field(row_targets, column_targets, initial_state)
        # solver = DfsSolver(field.copy(), "DFS")
        # solver.start()
        #
        # solver = BacktrackingSolver(field.copy(), "BacktrackingSolver")
        # solver.start()

        solver = ForwardCheckingSolver(field.copy(), "ForwardCheckingSolver")
        solver.start()
