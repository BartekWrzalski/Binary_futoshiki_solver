from Problems import variable
from copy import deepcopy


class Futoshiki:
    def __init__(self, futoshiki):
        self.variables = []
        self.horizontal_lines = []
        self.vertical_lines = []
        self.horizontal_dependencies = []
        self.vertical_dependencies = []
        self.possible_solutions = 0
        self.steps = 0

        self._create_variables(futoshiki)
        self._create_lines()

    def _create_variables(self, futoshiki):
        with open(futoshiki, encoding='utf-8') as file:
            self.size = int(len(file.readline()) / 2)
            file.seek(0)
            for i, line in enumerate(file):
                if i % 2 == 0:
                    self.variables.append([])
                    self.horizontal_dependencies.append([])
                    for char in line:
                        if char != '\n':
                            if char == '-' or char == '<' or char == '>':
                                self.horizontal_dependencies[-1].append(char)
                            else:
                                if char == 'x':
                                    vari = variable.Variable(char, [*range(1, self.size + 1)])
                                else:
                                    vari = variable.Variable(int(char), [int(char)])
                                self.variables[-1].append(vari)
                else:
                    for j, char in enumerate(line):
                        if char != '\n':
                            if i == 1:
                                self.vertical_dependencies.append([])
                            self.vertical_dependencies[j].append(char)

    def _create_lines(self):
        for i in range(self.size):
            self.horizontal_lines.append(self.get_line(i))
            self.vertical_lines.append(self.get_line(i, vertical=True))

    def get_line(self, i, vertical=False):
        if vertical:
            line = [self.variables[n][i].value for n in range(self.size)]
            return ''.join(list(map(str, line)))
        else:
            line = [v.value for v in self.variables[i]]
            return ''.join(list(map(str, line)))

    def check_restrictions(self, i, j):
        if self._check_line_restriction(i, j):
            return self._check_dependencies_restriction(i, j)
        return False

    def _check_line_restriction(self, i, j):
        if self.horizontal_lines[i].count(self.horizontal_lines[i][j]) > 1:
            return False
        if self.vertical_lines[j].count(self.vertical_lines[j][i]) > 1:
            return False
        return True

    def _check_dependencies_restriction(self, i, j):
        if j - 1 >= 0:
            if self.horizontal_dependencies[i][j - 1] == '>':
                if self.variables[i][j - 1].value < self.variables[i][j].value:
                    return False
            if self.horizontal_dependencies[i][j - 1] == '<':
                if self.variables[i][j - 1].value > self.variables[i][j].value:
                    return False

        if i - 1 >= 0:
            if self.vertical_dependencies[j][i - 1] == '>':
                if self.variables[i - 1][j].value < self.variables[i][j].value:
                    return False
            if self.vertical_dependencies[j][i - 1] == '<':
                if self.variables[i - 1][j].value > self.variables[i][j].value:
                    return False

        if j < self.size - 1:
            if self.variables[i][j + 1].value != 'x':
                if self.horizontal_dependencies[i][j] == '>':
                    if self.variables[i][j].value < self.variables[i][j + 1].value:
                        return False
                if self.horizontal_dependencies[i][j] == '<':
                    if self.variables[i][j].value > self.variables[i][j + 1].value:
                        return False

        if i < self.size - 1:
            if self.variables[i + 1][j].value != 'x':
                if self.vertical_dependencies[j][i] == '>':
                    if self.variables[i][j].value < self.variables[i + 1][j].value:
                        return False
                if self.vertical_dependencies[j][i - 1] == '<':
                    if self.variables[i][j].value > self.variables[i + 1][j].value:
                        return False
        return True

    def print(self):
        print(self.horizontal_lines[0][0], end='')
        for (dp, va) in zip(self.horizontal_dependencies[0], self.horizontal_lines[0][1:]):
            print(f'{dp}{va}', end='')

        print()
        for i in range(self.size - 1):
            for j in range(self.size):
                print(self.vertical_dependencies[j][i], end=' ')

            print(f'\n{self.horizontal_lines[i + 1][0]}', end='')
            for (dp, va) in zip(self.horizontal_dependencies[i + 1], self.horizontal_lines[i + 1][1:]):
                print(f'{dp}{va}', end='')
            print()

    def update_value(self, i, j, value='x'):
        self.variables[i][j].value = value
        self.horizontal_lines[i] = self.get_line(i)
        self.vertical_lines[j] = self.get_line(j, vertical=True)
        if value != 'x':
            self.variables[i][j].domain = [value]
        else:
            self.variables[i][j].domain = [*range(1, self.size + 1)]

    def initiate_domains(self):
        for i, line in enumerate(self.variables):
            for j, vari in enumerate(line):
                if vari.value != 'x':
                    self._update_value_line_restriction(i, j, vari.value)
                    self._update_value_dependencies_restrictions(i, j, vari.value)

    def _update_value_line_restriction(self, i, j, value):
        for vari in [v for v in self.variables[i] if v.value == 'x'] + \
                    [line[j] for line in self.variables if line[j].value == 'x']:
            if value in vari.domain:
                vari.domain.remove(value)
                if not vari.domain:
                    return False
        return True

    def _update_value_dependencies_restrictions(self, i, j, value):
        if i > 0:
            if self.variables[i - 1][j].value == 'x':
                if not self._update_value_dependencies_helper(i - 1, j, value, self.vertical_dependencies[j][i - 1]):
                    return False
        if i < self.size - 1:
            if self.variables[i + 1][j].value == 'x':
                if not self._update_value_dependencies_helper(i + 1, j, value, self.vertical_dependencies[j][i], higher=False):
                    return False
        if j > 0:
            if self.variables[i][j - 1].value == 'x':
                if not self._update_value_dependencies_helper(i, j - 1, value, self.horizontal_dependencies[i][j - 1]):
                    return False
        if j < self.size - 1:
            if self.variables[i][j + 1].value == 'x':
                if not self._update_value_dependencies_helper(i, j + 1, value, self.horizontal_dependencies[i][j], higher=False):
                    return False
        return True

    def _update_value_dependencies_helper(self, i, j, value, sign, higher=True):
        match sign:
            case '>':
                for v in deepcopy(self.variables[i][j].domain):
                    if v <= value and higher:
                        self.variables[i][j].domain.remove(v)
                    elif v >= value and not higher:
                        self.variables[i][j].domain.remove(v)
            case '<':
                for v in deepcopy(self.variables[i][j].domain):
                    if v >= value and higher:
                        self.variables[i][j].domain.remove(v)
                    elif v <= value and not higher:
                        self.variables[i][j].domain.remove(v)
        if not self.variables[i][j].domain:
            return False
        return True

    def update_domains(self, i, j):
        if self._update_value_line_restriction(i, j, self.variables[i][j].value):
            return self._update_value_dependencies_restrictions(i, j, self.variables[i][j].value)
        return False

    def reset_to_base_domains(self):
        domain = [*range(1, self.size + 1)]
        for line in self.variables:
            for vari in line:
                if vari == 'x':
                    vari.domain = domain

    def print_domains(self):
        for line in self.variables:
            for vari in line:
                print(F'{vari.domain!s:16}', end='\t\t')
            print()
