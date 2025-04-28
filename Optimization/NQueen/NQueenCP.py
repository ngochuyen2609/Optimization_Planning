from ortools.sat.python import cp_model

def solve_n_queens(n):
    model = cp_model.CpModel()

    x = {}
    for i in range(n):
        x[i] =  model.NewIntVar(1,n, f'x[{i}]')

    # Ràng buộc:
    model.AddAllDifferent(x[i] for i in range(n))
    model.AddAllDifferent([x[i] + i for i in range(n)])  #  \
    model.AddAllDifferent([x[i] - i for i in range(n)])  #  /

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print(n)
        for i in range(n):
            print(solver.Value(x[i]), end=' ')
    else:
        print("FAIL")


if __name__ == "__main__":
    n = int(input())
    solve_n_queens(n)