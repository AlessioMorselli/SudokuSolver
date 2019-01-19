from SudokuSolver import SudokuSolver
from threading import Thread

class ResolutionThread(Thread):
    def __init__(self, queue, sudokuSolver):
        Thread.__init__(self)
        self._queue = queue
        self._solver = sudokuSolver

    def run(self):
        self._solver.resolve_sudoku()
        sols = self._solver.retrieve_solution()
        self._queue.put(sols)