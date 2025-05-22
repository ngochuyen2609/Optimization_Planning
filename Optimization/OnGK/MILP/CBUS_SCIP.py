from ortools.linear_solver import pywraplp

def CBUS(numPassenger,numPlace,matrix):
    n =  2 * numPassenger + 1

    solver = pywraplp.Solver.CreateSolver('SAT')

    # Biến x[i,j] = 1 có đường từ i đến j
    x = {}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    #Biến t[i] = j thời điểm đến i laf j
    # 1 2 3 0
    t = {}
    for i in range(n):
        t[i] = solver.IntVar(1, n, f't[{i}]')

    #Biến p[i] số lượng khách trên xe
    p = {}
    for i in range(n):
        if i == 0:
            p[i] = solver.IntVar(0, 0, f'p[{i}]')
        else:
            p[i] = solver.IntVar(0, numPlace, f'p[{i}]')

    #Hàm mục tiêu:
    solver.Minimize(sum(x[i, j] * matrix[i][j]  for i in range(n) for j in range(n) if matrix[i][j] != 0))

    #RB: cân bằng luồng
    #(1,1)
    for i in range(n):
        solver.Add(sum(x[i, j] for j in range(n) if matrix[i][j] != 0) == 1)
        solver.Add(sum(x[j, i] for j in range(n) if matrix[j][i] != 0) == 1)

    #RB: tránh chu trình con
    # 0 1 2 3 4
    M = n * 1000
    for i in range(1, n):
        for j in range(n):
            if matrix[i][j] != 0:
                solver.Add(t[j] >= t[i] + 1 + (1 - x[i, j]) * (-M))

    #RB: đón trước trả
    for i in range(1, numPassenger + 1):
        solver.Add(t[i + numPassenger] >= t[i] + 1)

    #RB: số lượng khách trên xe
    # đón khách : p[j] = p[i] + 1 nếu có x[i,j] = 1 và j là điểm đón
    # trả khách : p[j] = p[i] - 1 nếu có x[i,j] = 1 và j là điểm trả
    for j in range(1, numPassenger + 1):
        for i in  range(n):
            if matrix[i][j] != 0:
                solver.Add(p[j] >= p[i] + 1 - M * (1 - x[i, j]))
                solver.Add(p[j] <= p[i] + 1 + M * (1 - x[i, j]))

    for j in range(numPassenger + 1, n):
        for i in range(n):
            if matrix[i][j] != 0:
                solver.Add(p[j] >= p[i] - 1 - M * (1 - x[i, j]))
                solver.Add(p[j] <= p[i] - 1 + M * (1 - x[i, j]))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
    else:
        print('-1')


if __name__ == "__main__":
    numPassenger, numPlace = map(int, input().split())
    matrix = []
    for i in range(2 * numPassenger + 1):
        matrix.append(list(map(int, input().split())))

    CBUS(numPassenger,numPlace,matrix)