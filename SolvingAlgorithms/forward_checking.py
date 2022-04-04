import math
from copy import deepcopy

class Forward:
    def __init__(self):
        self._possible_solutions = 0
        self._steps = 0

    def forward_checking(self, problem, choose_variable='sequence', choose_value='sequence'):
        problem.initiate_fields()
        match choose_variable, choose_value:
            case 'sequence', 'sequence':
                self._forward_algorithm(problem, self._get_next_variable_from_sequence, self._get_values_in_sequence)
            case 'small_field', 'sequence':
                self._forward_algorithm(problem, self._get_next_variable_by_field, self._get_values_in_sequence)
            case 'sequence', 'low_occurrence':
                self._forward_algorithm(problem, self._get_next_variable_from_sequence, self._get_value_by_occurrence)
            case 'small_field', 'low_occurrence':
                self._forward_algorithm(problem, self._get_next_variable_by_field, self._get_value_by_occurrence)
            case _:
                print(f'Not existing mode: {choose_variable}, {choose_value}')
        problem.reset_to_base_fields()

    def _get_next_variable_from_sequence(self, problem):
        for i, line in enumerate(problem.variables):
            for j, vari in enumerate(line):
                if vari.value == 'x':
                    return vari, i, j
        return None, None, None

    def _get_next_variable_by_field(self, problem):
        field_size = math.inf
        var_to_send = None
        ix = jx = None

        for i, line in enumerate(problem.variables):
            for j, vari in enumerate(line):
                if vari.value == 'x':
                    vari_field_size = len(vari.field)
                    if vari_field_size == 1:
                        return vari, i, j

                    if vari_field_size < field_size:
                        field_size = vari_field_size
                        var_to_send = vari
                        ix = i
                        jx = j
        return var_to_send, ix, jx

    def _get_values_in_sequence(self, problem, i, j):
        return problem.variables[i][j].field

    def _get_value_by_occurrence(self, problem, i, j):
        values = problem.variables[i][j].field
        if len(values) == 0:
            return values

        values_in_line = ''.join([str(v) for vari in problem.variables[i] for v in vari.field])
        for ix, line in enumerate(problem.variables):
            if i != ix:
                values_in_line += ''.join([str(v) for v in line[j].field])

        return sorted(values, key=lambda k: values_in_line.count(str(k)))

    def _forward_algorithm(self, problem, choose_variable, value_field):
        self._possible_solutions = 0
        self._steps = 0

        def recursive_forward(vari, i, j):
            for v in value_field(problem, i, j):
                bf_var_problem = deepcopy(problem.variables)
                self._steps += 1
                problem.update_value(i, j, v)
                if problem.update_fields(i, j):
                    vv, ii, jj = choose_variable(problem)
                    if vv is None:
                        self._possible_solutions += 1
                        self._print_result(problem)
                        problem.variables = bf_var_problem
                        return
                    recursive_forward(vv, ii, jj)
                problem.variables = bf_var_problem
                problem.update_value(i, j)
            self._steps += 1

        va, ix, jx = choose_variable(problem)
        recursive_forward(va, ix, jx)

    def _print_result(self, problem):
        print(f'Steps: {self._steps}')
        print(f'Solution: {self._possible_solutions}')
        problem.print()
        print()
