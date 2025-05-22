from ortools.linear_solver import pywraplp

def TSP(numPoint, matrix):
    solver = pywraplp.Solver.CreateSolver('SAT')

    #biến x[i,j] = 1
    x = {}
    for i in range(numPoint):
        for j in range(numPoint):
            if matrix[i][j] != 0:
                x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    #t[i] đánh dấu thời gian đến i
    # 0 1 2 3 1230
    t = {}
    for i in range(numPoint):
        t[i] = solver.IntVar(1, numPoint, f't[{i}]')

    # Hàm mục tiêu:
    solver.Minimize(sum(x[i,j] * matrix[i][j] for i in range(numPoint) for j in range(numPoint) if matrix[i][j] != 0))

    #RB: Cân bằng luồng
    for i in range(numPoint):
        solver.Add(sum(x[i, j] for j in range(numPoint) if matrix[i][j] != 0) == 1)
        solver.Add(sum(x[j, i] for j in range(numPoint) if matrix[i][j] != 0) == 1)

    #RB: Tránh chu trình con
    # t[j] = t[i] + 1 nếu x[i,j] = 1
    M = numPoint * 10000
    for i in range(1, numPoint):
        for j in range(numPoint):
            if matrix[i][j] != 0:
                solver.Add(t[j] >= t[i] + 1 + (x[i,j] - 1) * M)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
        # print(numPoint)
        # curr = 0
        # result = [0]
        # while (len(result) < numPoint):
        #     for i in range(numPoint):
        #         if matrix[curr][i] != 0:
        #             if (x[curr, i].solution_value() == 1):
        #                 curr = i
        #                 result.append(i)
        #                 break
        #
        # result.append(0)
        # for i in range(1,len(result) - 1):
        #     print(result[i]  , end=' ')
    else :
        print(-1)

if __name__ == '__main__':
    numPoint = int(input())
    matrix = []
    for i in range(numPoint):
        matrix.append(list( map(int, input().split() ) ))

    TSP(numPoint, matrix)