from cspsolver import CSPSolver, Algorithm, Policy

class SudokuSolver(CSPSolver):
    def __init__(self):
        super(SudokuSolver, self).__init__(Algorithm.AC3, Policy.MinimumRemainingValues)

        for i in range(1, 10):
            for j in range(1, 10):
                self.add_variable("cell_" + str(i) + str(j), list(range(1, 10)))

        different = lambda x, y: x != y
        for i in range(1, 10):
            for j in range(1, 10):
                for k in range(j, 10):
                    self.add_constraint(("cell_" + str(i) + str(j), "cell_" + str(i) + str(k)), different)
                    self.add_constraint(("cell_" + str(j) + str(i), "cell_" + str(k) + str(i)), different)

        start = [1, 4, 7, 10]

        for r in range(3):
            for i in range(start[r], start[r + 1]):
                for c in range(3):
                    for j in range(start[c], start[c + 1]):
                        for k in range(start[r], start[r + 1]):
                            for h in range(start[c], start[c + 1]):
                                c1, c2 = self._constraints.get_binary_constraints("cell_" + str(i) + str(j), "cell_" + str(k) + str(h))
                                if not (c1 or c2):
                                    self.add_constraint(("cell_" + str(i) + str(j), "cell_" + str(k) + str(h)), different)
    
    def add_known_number(self, line, column, number):
        self.add_constraint(("cell_" + str(line) + str(column),), lambda x: x == number)
    
    def resolve_sudoku(self):
        self.apply_node_consistency()
        self.apply_arc_consistency()

        self.solve()

    def retrieve_solution(self):
        if not self._found_solution:
            return []
        
        solution_node = self._solutions[0]
        solutions = [[0 for j in range(1, 10)] for i in range(1, 10)]

        for i in range(1, 10):
            for j in range(1, 10):
                solutions[i - 1][j - 1] = solution_node.get_variable_by_name("cell_" + str(i) + str(j)).value
        
        return solutions

if __name__ == '__main__':
    ss = SudokuSolver()

    ss.add_known_number(1, 5, 6)
    ss.add_known_number(1, 8, 2)
    ss.add_known_number(1, 9, 7)

    ss.add_known_number(2, 2, 5)
    ss.add_known_number(2, 3, 7)
    ss.add_known_number(2, 9, 4)

    ss.add_known_number(3, 1, 8)
    ss.add_known_number(3, 4, 9)

    ss.add_known_number(4, 2, 1)
    ss.add_known_number(4, 3, 3)
    ss.add_known_number(4, 6, 4)

    ss.add_known_number(6, 4, 7)
    ss.add_known_number(6, 7, 5)
    ss.add_known_number(6, 8, 6)

    ss.add_known_number(7, 6, 5)
    ss.add_known_number(7, 9, 3)

    ss.add_known_number(8, 1, 7)
    ss.add_known_number(8, 7, 2)
    ss.add_known_number(8, 8, 9)

    ss.add_known_number(9, 1, 4)
    ss.add_known_number(9, 2, 6)
    ss.add_known_number(9, 5, 7)

    ss.resolve_sudoku()
    ss.print_solutions()

    sols = ss.retrieve_solution()

    print(sols)