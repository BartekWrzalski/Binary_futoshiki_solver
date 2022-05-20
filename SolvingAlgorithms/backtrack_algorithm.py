import time


class Backtrack:
    def __init__(self):
        self._possible_solutions = 0
        self._steps = 0
        self._start = 0

    def backtrack_searching(self, problem):
        self._possible_solutions = 0
        self._steps = 0
        self._start = time.time()

        def recursive_backtrack(i, j):
            if problem.variables[i][j].value == 'x':
                for va in problem.variables[i][j].domain:
                    problem.update_value(i, j, va)
                    self._steps += 1
                    if problem.check_restrictions(i, j):
                        if i == problem.size - 1 and j == problem.size - 1:
                            self._possible_solutions += 1
                            # self._print_result(problem)
                            self._print_stats()
                            problem.update_value(i, j, 'x')
                            return
                        elif j == problem.size - 1:
                            recursive_backtrack(i + 1, 0)
                        else:
                            recursive_backtrack(i, j + 1)
                problem.update_value(i, j, 'x')
                self._steps += 1
            else:
                if i == problem.size - 1 and j == problem.size - 1:
                    self._possible_solutions += 1
                    self._print_result(problem)
                    problem.update_value(i, j, 'x')
                    return
                elif j == problem.size - 1:
                    recursive_backtrack(i + 1, 0)
                else:
                    recursive_backtrack(i, j + 1)

        recursive_backtrack(0, 0)

    def _print_result(self, problem):
        print(f'Steps: {self._steps}')
        print(f'Solution: {self._possible_solutions}')
        problem.print()
        print()

    def _print_stats(self):
        print(f'{self._possible_solutions:5} {self._steps:11}   {round(time.time() - self._start, 3)}')
