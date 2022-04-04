from Problems import variable
from copy import deepcopy


class Binary:
    def __init__(self, binary):
        self.variables = []
        self.horizontal_lines = []
        self.vertical_lines = []
        self.possible_solutions = 0
        self.steps = 0

        self._create_variables(binary)
        self._create_lines()

    def _create_variables(self, binary):
        with open(binary, encoding='utf-8') as file:
            for line in file:
                self.variables.append([])
                for char in line:
                    if char != '\n':
                        if char == 'x':
                            vari = variable.Variable(char, [0, 1])
                        else:
                            vari = variable.Variable(int(char), [int(char)])
                        self.variables[len(self.variables) - 1].append(vari)
        self.size = len(self.variables)

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
            if self._check_triple_value_restriction(i, j):
                return self._check_identity_restriction(i, j)
        return False

    def _check_triple_value_restriction(self, i, j):
        if '111' in self.horizontal_lines[i] or '000' in self.horizontal_lines[i]:
            return False
        if '111' in self.vertical_lines[j] or '000' in self.vertical_lines[j]:
            return False
        return True

    def _check_identity_restriction(self, i, j):
        if i == self.size - 1:
            for ix in range(self.size):
                if i != ix:
                    if self.horizontal_lines[ix] == self.horizontal_lines[i]:
                        return False
        elif j == self.size - 1:
            for jx in range(self.size):
                if j != jx:
                    if self.vertical_lines[jx] == self.vertical_lines[j]:
                        return False
        return True

    def _check_line_restriction(self, i, j):
        if self.horizontal_lines[i].count('1') > self.size / 2 \
                or self.horizontal_lines[i].count('0') > self.size / 2:
            return False
        if self.vertical_lines[j].count('1') > self.size / 2 \
                or self.vertical_lines[j].count('0') > self.size / 2:
            return False
        return True

    def print(self):
        for line in self.horizontal_lines:
            print(line)

    def update_value(self, i, j, value='x'):
        self.variables[i][j].value = value
        self.horizontal_lines[i] = self.get_line(i)
        self.vertical_lines[j] = self.get_line(j, vertical=True)
        if value != 'x':
            self.variables[i][j].domain = [value]
        else:
            self.variables[i][j].domain = [0, 1]

    def initiate_domains(self):
        for i, line in enumerate(self.variables):
            for j, vari in enumerate(line):
                if vari.value != 'x':
                    self._update_value_triple_value_restriction(i, j, vari.value)
                    self._update_value_line_restriction(i, j, vari.value)
                    self._check_identity_restriction(i, j)

    def _update_value_triple_value_restriction(self, i, j, value):
        if j - 1 >= 0:
            if j - 2 >= 0:
                if not self._update_value_triple_helper_long(value, i, 0, 0, 0, j, -1, -2, 1):
                    return False
            else:
                if not self._update_value_triple_helper_short(value, i, 0, j, -1):
                    return False
        if i - 1 >= 0:
            if i - 2 >= 0:
                if not self._update_value_triple_helper_long(value, i, -1, -2, 1, j, 0, 0, 0):
                    return False
            else:
                if not self._update_value_triple_helper_short(value, i, -1, j, 0):
                    return False
        if j + 1 < self.size:
            if j + 2 < self.size:
                if not self._update_value_triple_helper_long(value, i, 0, 0, 0, j, 1, 2, -1):
                    return False
            else:
                if not self._update_value_triple_helper_short(value, i, 0, j, 1):
                    return False
        if i + 1 < self.size:
            if i + 2 < self.size:
                if not self._update_value_triple_helper_long(value, i, 1, 2, -1, j, 0, 0, 0):
                    return False
            else:
                if not self._update_value_triple_helper_short(value, i, 1, j, 0):
                    return False
        return True

    def _update_value_triple_helper_long(self, value, i, i_mod1, i_mod2, i_mod1r, j, j_mod1, j_mod2, j_mod1r):
        if self.variables[i + i_mod2][j + j_mod2].value == value:
            if value in self.variables[i + i_mod1][j + j_mod1].domain:
                self.variables[i + i_mod1][j + j_mod1].domain.remove(value)
                if not self.variables[i + i_mod1][j + j_mod1].domain:
                    return False
        elif self.variables[i + i_mod1][j + j_mod1].value == value:
            if value in self.variables[i + i_mod2][j + j_mod2].domain:
                self.variables[i + i_mod2][j + j_mod2].domain.remove(value)
                if not self.variables[i + i_mod2][j + j_mod2].domain:
                    return False
            if (self.size - 1 > j > 0 and j_mod1r) or (self.size - 1 > i > 0 and i_mod1r):
                if value in self.variables[i + i_mod1r][j + j_mod1r].domain:
                    self.variables[i + i_mod1r][j + j_mod1r].domain.remove(value)
                    if not self.variables[i + i_mod1r][j + j_mod1r].domain:
                        return False
        return True

    def _update_value_triple_helper_short(self, value, i, i_mod, j, j_mod):
        if self.variables[i + i_mod][j + j_mod].value == value:
            if value in self.variables[i - i_mod][j - j_mod].domain:
                self.variables[i - i_mod][j - j_mod].domain.remove(value)
                if not self.variables[i - i_mod][j - j_mod].domain:
                    return False
        return True

    def _update_value_line_restriction(self, i, j, value):
        if self.horizontal_lines[i].count(str(value)) == self.size / 2:
            for vari in [v for v in self.variables[i] if v.value == 'x']:
                if value in vari.domain:
                    vari.domain.remove(value)
                    if not vari.domain:
                        return False
        if self.vertical_lines[j].count(str(value)) == self.size / 2:
            for vari in [line[j] for line in self.variables if line[j].value == 'x']:
                if value in vari.domain:
                    vari.domain.remove(value)
                    if not vari.domain:
                        return False
        return True

    def update_domains(self, i, j):
        if self._update_value_triple_value_restriction(i, j, self.variables[i][j].value):
            if self._update_value_line_restriction(i, j, self.variables[i][j].value):
                return self._check_identity_restriction(i, j)
        return False

    def reset_to_base_domains(self):
        for line in self.variables:
            for vari in line:
                if vari == 'x':
                    vari.domain = [0, 1]

    def print_domains(self):
        for line in self.variables:
            for vari in line:
                print(F'{vari.domain!s:8}', end='\t\t')
            print()
