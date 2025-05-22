from ortools.sat.python import cp_model

def nQueen(n):
    model = cp_model.CpModel()

    # x[i] = j con hậu ở cột i thì ở hàng j
    x = {}
    for i in range(n):
        x[i] = model.NewIntVar(0, n - 1, f'x[{i}]')

    #RB: các con hậu không nằm trên một hàng
    model.AddAllDifferent(x[i] for i in range(n))

    #RB: các con hậu không nằm trên đường chéo /
    model.AddAllDifferent((x[i] + i) for i in range(n))

    #RB: các con hậu không nằm trên đường chéo \
    model.AddAllDifferent((x[i] - i) for i in range(n))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.OPTIMAL:
        for i in range(n):
            stt = solver.Value(x[i])
            for i in range(stt):
                print(0, end=' ')
            print(1, end=' ')
            for i in range(n - stt -1):
                print(0, end=' ')
            print()
    else:
        print(-1)


if __name__ == '__main__':
    n = 8

    nQueen(n)