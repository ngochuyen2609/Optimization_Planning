from ortools.sat.python import cp_model
def Sudoku():
    model = cp_model.CpModel()

    # x[i, j] = k ở vị trí i,j điền số k
    x = {}
    for i in range(9):
        for j in range(9):
            x[i, j] = model.NewIntVar(1, 9, f'x[{i},{j}]')

    #RB: cùng hàng, cùng cột thì không cùng số
    for i in range(9):
        model.AddAllDifferent(x[i, j] for j in range(9))
        model.AddAllDifferent(x[j, i] for j in range(9))

    #RB: cùng 1 ô vuông thì không cùng số
    for i in range(3):
        for j in range(3):
            model.AddAllDifferent(x[u + i * 3,v + j * 3] for u in range(3) for v in range(3))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(9):
            for j in range(9):
                print(int(solver.Value(x[i ,j])),end = ' ')
            print()

    else:
        print(-1)

if __name__ == '__main__':
    Sudoku()