from ResolutionThread import ResolutionThread
from SudokuSolver import SudokuSolver
from tkinter import *
import tkinter.ttk
from queue import Queue, Empty

class UI():
    def __init__(self):
        self._root = Tk()
        self._root.title("Sudoku Solver")
        self._current_frame = Frame(self._root)
    
    def _clear(self):
        self._current_frame.destroy()
        self._current_frame = Frame(self._root)

    def _draw_current_frame(self):
        self._current_frame.pack(fill = BOTH, expand = 1)
    
    def _filler(self, n_row, colspan):
        Label(self._current_frame, text=" ").grid(row = n_row, columnspan = colspan)

    def _waiting(self):
        self._clear()

        Label(self._current_frame, text="I am resolving a sudoku...").grid(row = 0)

        self._filler(1, 1)

        pb = tkinter.ttk.Progressbar(self._current_frame, orient='horizontal', mode='indeterminate', length = 400)
        pb.grid(row = 2)
        pb.start(25)

        self._filler(3, 1)

        self._draw_current_frame()
    
    def _draw_sudoku_input(self):
        self._clear()

        cells_entry = [[Entry(self._current_frame, width = 5, justify = CENTER) for j in range(0, 9)] for i in range(0, 9)]

        n_ver_seps = 1
        n_hor_seps = 1

        for i in range(0, 9):
            n_ver_seps = 1
            if (i) % 3 == 0:
                n_hor_seps += 1
            for j in range(0, 9):
                if (j) % 3 == 0:
                    n_ver_seps += 1
                cells_entry[i][j].grid(row = i - 1 + n_hor_seps, column = j - 1 + n_ver_seps)

        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 0, column = 0, columnspan = 9 + 4, sticky="ew")
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 4, column = 0, columnspan = 9 + 4, sticky="ew")
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 8, column = 0, columnspan = 9 + 4, sticky="ew")
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 12, column = 0, columnspan = 9 + 4, sticky="ew")

        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 0, row = 0, rowspan = 9 + 4, sticky="ns")
        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 4, row = 0, rowspan = 9 + 4, sticky="ns")
        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 8, row = 0, rowspan = 9 + 4, sticky="ns")
        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 12, row = 0, rowspan = 9 + 4, sticky="ns")

        n = 13

        self._filler(n, 9)

        quit_button = Button(self._current_frame, text='Stop', command = self._root.quit)
        quit_button.grid(row = n + 1, column = 6)

        resolve_button = Button(self._current_frame, text='Calc', command = lambda ce = cells_entry: self._calc_solution(ce))
        resolve_button.grid(row = n + 1, column = 3)

        self._filler(n + 2, 9)

        self._draw_current_frame()
    
    def _calc_solution(self, cells_entry):
        solutions_queue = Queue()

        def process_queue():
            try:
                sols = solutions_queue.get(0)
                self._draw_solution(sols)
            except Empty:
                self._root.after(100, lambda : process_queue())

        ss = SudokuSolver()

        for i in range(0, 9):
            for j in range(0, 9):
                value = cells_entry[i][j].get()
                if value:
                    ss.add_known_number(i + 1, j + 1, int(value))

        ResolutionThread(solutions_queue, ss).start()
        self._waiting()

        self._root.after(100, lambda : process_queue())
    
    def _draw_solution(self, sols):
        self._clear()

        n_ver_seps = 1
        n_hor_seps = 1

        for i in range(0, 9):
            n_ver_seps = 1
            if (i) % 3 == 0:
                n_hor_seps += 1
            for j in range(0, 9):
                if (j) % 3 == 0:
                    n_ver_seps += 1
                l = Label(self._current_frame, text = str(sols[i][j]), width = 5, justify = CENTER)
                l.grid(row = i - 1 + n_hor_seps, column = j - 1 + n_ver_seps)
        
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 0, column = 0, columnspan = 9 + 4, sticky="ew")
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 4, column = 0, columnspan = 9 + 4, sticky="ew")
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 8, column = 0, columnspan = 9 + 4, sticky="ew")
        tkinter.ttk.Separator(self._current_frame, orient = HORIZONTAL).grid(row = 12, column = 0, columnspan = 9 + 4, sticky="ew")

        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 0, row = 0, rowspan = 9 + 4, sticky="ns")
        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 4, row = 0, rowspan = 9 + 4, sticky="ns")
        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 8, row = 0, rowspan = 9 + 4, sticky="ns")
        tkinter.ttk.Separator(self._current_frame, orient = VERTICAL).grid(column = 12, row = 0, rowspan = 9 + 4, sticky="ns")

        n = 13

        self._filler(n, 9 + 4)

        quit_button = Button(self._current_frame, text='Stop', command = self._root.quit)
        quit_button.grid(row = n + 1, column = 6)

        new_button = Button(self._current_frame, text='New', command = self._draw_sudoku_input)
        new_button.grid(row = n + 1, column = 3)

        self._filler(n + 2, 9 + 4)

        self._draw_current_frame()

    def mainloop(self):
        self._draw_sudoku_input()
        self._root.mainloop()
