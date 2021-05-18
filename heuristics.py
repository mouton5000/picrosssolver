def _lefter(size, line):
    t = [-1 for _ in range(size)]
    c = 0
    id = 0
    for x in line:
        for _ in range(x):
            t[c] = id
            c += 1
        id += 1
        c += 1
    return t


def _righter(size, line):
    t = [-1 for _ in range(size)]
    c = len(t) - 1
    id = len(line) - 1
    for x in reversed(line):
        for _ in range(x):
            t[c] = id
            c -= 1
        id -= 1
        c -= 1
    return t


def intersection(size, line):
    t = [-1 for _ in range(size)]
    l = _lefter(size, line)
    r = _righter(size, line)
    for i, c in enumerate(zip(l, r)):
        cl, cr = c
        if cl == cr and cl >= 0:
            t[i] = 1

    return t


def intersections(picross, solution):
    for i, line in enumerate(picross.lines):
        inters = intersection(picross.width, line)
        for j, x in enumerate(inters):
            if x != 1:
                continue
            solution[i][j] = 1

    for j, column in enumerate(picross.columns):
        inters = intersection(picross.height, column)
        for i, x in enumerate(inters):
            if x != 1:
                continue
            solution[i][j] = 1


def heuristics(picross, solution):
    intersections(picross, solution)
    return solution
