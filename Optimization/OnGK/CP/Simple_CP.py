from ortools.sat.python import cp_model

def CP(domain):
    model = cp_model.CpModel()

    # Biến x1, x2, x3, x4, x5
    x = {}
    for i in range(5):
        x[i] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain),f'x[{i}]')

    model.Add(x[2] + 3 != x[1])
    model.Add(x[3] <= x[4])
    model.Add(x[2] + x[3] == x[0] + 1)
    model.Add(x[4] <= 3)
    model.Add(x[1] + x[4] == 7)

    x2_equal_1 = model.NewBoolVar(f'x2_equal_1')
    model.Add(x[2] == 1).OnlyEnforceIf(x2_equal_1)
    model.Add(x[2] != 1).OnlyEnforceIf(x2_equal_1.Not())

    x4_not_equal_2 = model.NewBoolVar(f'x4_not_equal_2')
    model.Add(x[4] != 2).OnlyEnforceIf(x4_not_equal_2)
    model.Add(x[4] == 2).OnlyEnforceIf(x4_not_equal_2.Not())

    model.AddImplication(x2_equal_1,x4_not_equal_2)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for i in range(5):
            print(solver.Value(x[i]), end=' ')

    else:
        print(-1)

if __name__ == '__main__':
    x = [1, 2, 3, 4, 5]

    CP(x)