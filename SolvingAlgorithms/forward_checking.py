import math
import pickle
import time


class Forward:
    def __init__(self):
        self._possible_solutions = 0
        self._steps = 0
        self._start = 0

    def forward_checking(self, problem, choose_variable='sequence', choose_value='sequence'):
        problem.initiate_domains()
        self._start = time.time()
        match choose_variable, choose_value:
            case 'sequence', 'sequence':
                self._forward_algorithm(problem, self._get_next_variable_from_sequence, self._get_values_in_sequence)
            case 'small_domain', 'sequence':
                self._forward_algorithm(problem, self._get_next_variable_by_domain, self._get_values_in_sequence)
            case 'sequence', 'low_occurrence':
                self._forward_algorithm(problem, self._get_next_variable_from_sequence, self._get_value_by_occurrence)
            case 'small_domain', 'low_occurrence':
                self._forward_algorithm(problem, self._get_next_variable_by_domain, self._get_value_by_occurrence)
            case _:
                print(f'Not existing mode: {choose_variable}, {choose_value}')
        problem.reset_to_base_domains()

    def _get_next_variable_from_sequence(self, problem):
        for i, line in enumerate(problem.variables):
            for j, vari in enumerate(line):
                if vari.value == 'x':
                    return vari, i, j
        return None, None, None

    def _get_next_variable_by_domain(self, problem):
        domain_size = math.inf
        var_to_send = None
        ix = jx = None

        for i, line in enumerate(problem.variables):
            for j, vari in enumerate(line):
                if vari.value == 'x':
                    vari_domain_size = len(vari.domain)
                    if vari_domain_size == 1:
                        return vari, i, j

                    if vari_domain_size < domain_size:
                        domain_size = vari_domain_size
                        var_to_send = vari
                        ix = i
                        jx = j
        return var_to_send, ix, jx

    def _get_values_in_sequence(self, problem, i, j):
        return problem.variables[i][j].domain

    def _get_value_by_occurrence(self, problem, i, j):
        values = problem.variables[i][j].domain
        if len(values) == 0:
            return values

        values_in_line = ''.join([str(v) for vari in problem.variables[i] for v in vari.domain])
        for ix, line in enumerate(problem.variables):
            if i != ix:
                values_in_line += ''.join([str(v) for v in line[j].domain])

        return sorted(values, key=lambda k: values_in_line.count(str(k)))

    def _forward_algorithm(self, problem, choose_variable, value_domain):
        self._possible_solutions = 0
        self._steps = 0

        def recursive_forward(i, j):
            for v in value_domain(problem, i, j):
                bf_var_problem = pickle.loads(pickle.dumps(problem.variables))
                self._steps += 1
                problem.update_value(i, j, v)
                if problem.update_domains(i, j):
                    vv, ii, jj = choose_variable(problem)
                    if vv is None:
                        self._possible_solutions += 1
                        # self._print_result(problem)
                        self._print_stats()
                        problem.variables = bf_var_problem
                        return
                    recursive_forward(ii, jj)
                problem.variables = bf_var_problem
                problem.update_value(i, j)
            self._steps += 1

        va, ix, jx = choose_variable(problem)
        recursive_forward(ix, jx)

    def _print_result(self, problem):
        print(f'Solution: {self._possible_solutions}')
        print(f'Steps: {self._steps}')
        problem.print()
        print()

    def _print_stats(self):
        print(f'{self._possible_solutions:5} {self._steps:11}   {round(time.time() - self._start, 3)}')
