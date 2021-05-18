# This is a sample Python script.
import itertools
from heuristics import *
from copy import deepcopy


class SolutionNode:

    nb = 0

    def __init__(self, picross, solution):
        SolutionNode.nb += 1

        self.nb = SolutionNode.nb
        self.picross = picross

        w = picross.wrong(solution)
        #print(self, solution, w)
        if picross.wrong(solution):
            self.solution = None
        else:
            heuristics(picross, solution)
            self.solution = solution
            #print(">>>", solution)

    def __str__(self):
        return str(self.nb)

    def explore(self):

        if self.solution is None:
            return None

        if all(self.solution[i][j] != 0 for i in range(self.picross.height) for j in range(self.picross.width)):
            return self.solution

        for i in range(self.picross.height):
            for j in range(self.picross.width):
                if self.solution[i][j] == 0:
                    #print(self, i, j, 1)

                    cp1 = deepcopy(self.solution)
                    cp1[i][j] = 1
                    sol1 = SolutionNode(self.picross, cp1).explore()

                    if sol1 is not None:
                        return sol1

                    #print(self, i, j, -1)
                    cp2 = deepcopy(self.solution)
                    cp2[i][j] = -1
                    sol2 = SolutionNode(self.picross, cp2).explore()
                    if sol2 is not None:
                        return sol2
                    return None

        return None


class Picross:
    def __init__(self):
        self.lines = []
        self.columns = []

    def add_line(self):
        self.lines.append([])

    def add_column(self):
        self.columns.append([])

    def add_line_number(self, i, x):
        self.lines[i].append(x)

    def add_column_number(self, i, x):
        self.columns[i].append(x)

    def read_solved_picross(self, filename):
        with open(filename, 'r') as f:
            lines = list((x.strip() for x in f))

        columns = [[] for _ in range(len(lines[0]))]
        for i, line in enumerate(lines):
            self.add_line()
            x = 0
            for c, g in itertools.groupby(line):
                nb = len(list(g))
                if c == 'X':
                    self.add_line_number(i, nb)
                for j in range(x, x + nb):
                    columns[j].append(c)
                x += nb

        for i, column in enumerate(columns):
            self.add_column()
            for c, g in itertools.groupby(column):
                if c != 'X':
                    continue
                nb = len(list(g))
                self.add_column_number(i, nb)

        #for line in self.lines:
        #    print("L", line)
        #for column in self.columns:
        #    print("C", column)

    @property
    def width(self):
        return len(self.columns)

    @property
    def height(self):
        return len(self.lines)

    def solve(self):
        rootSolution = [[0 for _ in range(self.width)] for _ in range(self.height)]
        root = SolutionNode(self, rootSolution)
        return root.explore()

    def wrong(self, solution):

        def sublist(l1, l2):
            ''' Renvoie vrai si l1 est une sous liste de l2 '''
            if l1 == []:
                return True
            if len(l1) > len(l2):
                return False
            if l1[0] == l2[0] and sublist(l1[1:], l2[1:]):
                return True
            return sublist(l1, l2[1:])

        def check(line, solline):
            values = []
            v = 0
            b = True

            for c in solline:
                if c == -1:
                    if b and v != 0:
                        values.append(v)
                    v = 0
                    b = True
                elif c == 1:
                    v += 1
                    if len(line) == 0 or v > max(line):
                        return False
                elif c == 0:
                    b = False
                    v = 0
            if b and v != 0:
                values.append(v)

            if any(c == 0 for c in solline):
                lst = [x for x in line if x in values]
                return sublist(values, lst)
            else:
                return values == line

        return any(not check(line, [solution[i][j] for j in range(self.width)]) for i, line in enumerate(self.lines)) \
        or any(not check(column, [solution[i][j] for i in range(self.height)]) for j, column in enumerate(self.columns))

    def __str__(self):
        return str(self.lines) + str(self.columns)


def print_solution(sol):
    def c(x):
        return 'X' if x == 1 else '.'

    for line in sol:
        print(''.join([c(x) for x in line]))


if __name__ == '__main__':
    p = Picross()
    p.read_solved_picross("picross1")
    sol = p.solve()
    print("Noeuds explorés : ", SolutionNode.nb)
    print_solution(sol)
