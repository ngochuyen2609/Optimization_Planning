from ortools.linear_solver import pywraplp


def sloveTSP(places, capacity, conflict, conflicts):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Khai bao bien: x[i,j] == 1 di duoc tu i den j
    x = {}
    for i in range(places):
        for j in range(places):
            if capacity[i][j] != 0 and i != j:
                x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')
            else:
                x[i, j] = solver.IntVar(0, 0, f'x[{i},{j}]')

    # Khai bao bien : t[i] thoi diem den thanh pho i
    # t[0] = 0
    t = {}
    t[0] = solver.IntVar(0, 0, f't[{0}]')
    for i in range(1, places):
        t[i] = solver.IntVar(1, places - 1, f't[{i}]')

    # Ham muc tieu:
    solver.Minimize(solver.Sum(x[i, j] * capacity[i][j] for i in range(places) for j in range(places)))

    # RB: chi di qua moi thanh pho 1 lan
    for i in range(places):
        solver.Add(solver.Sum(x[i, j] for j in range(places)) == 1)
        solver.Add(solver.Sum(x[j, i] for j in range(places)) == 1)

    # RB: tranh chu trinh con
    # t[j]= t[i] + 1 neu x[i,j] == 1
    M = 1e9
    for i in range(places):
        for j in range(1, places):
            solver.Add(t[j] >= t[i] + 1 - (1 - x[i, j]) * M)

    #RB: ddi i truoc j
    for (i, j) in conflicts:
        solver.Add(t[i] <= t[j] - 1)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(solver.Objective().Value())
        curr = 0
        result = [0]
        while(len(result) < places):
            for i in range(places):
                if x[curr, i].solution_value() == 1:
                    result.append(i)
                    curr = i
                    break
        for i in range(places):
            print(t[i].solution_value(), end =' ')
        print()
        for i in result:
            print(i + 1, end=' ')
        return
    else:
        print(-1)
        return


if __name__ == "__main__":
    places = int(input())
    capacity = []
    for i in range(places):
        capacity.append(list(map(int, input().split())))
    conflict = int(input())
    conflicts = []
    for i in range(conflict):
        conflicts.append(list(map(int, input().split())))

    sloveTSP(places, capacity, conflict, conflicts)