from ortools.sat.python import cp_model

def sol():
    n = 9
    model = cp_model.CpModel()

    # Khai báo biến
    x = {(i, j): model.NewIntVar(1, 9, f'x[{i},{j}]') for i in range(n) for j in range(n)}

    # Ràng buộc
    for i in range(n):
        model.AddAllDifferent([x[i, j] for j in range(n)])
        model.AddAllDifferent([x[j, i] for j in range(n)])
    for r in range(0, n, 3):
        for c in range(0, n, 3):
            model.AddAllDifferent([x[r+i, c+j] for i in range(3) for j in range(3)])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for i in range(n):
            for j in range(n):
                print(solver.Value(x[i, j]), end=' ')
            print()
    else:
        print('FAIL')

if __name__ == '__main__':
    sol()