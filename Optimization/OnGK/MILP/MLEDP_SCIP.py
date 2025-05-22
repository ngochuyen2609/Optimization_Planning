from ortools.linear_solver import pywraplp

def Balance(solver, x,numNode, matrix):
    # RB: các đường đi đều bắt đàu từ 1 kết thúc là n
    # (1,0) (0,1)
    solver.Add((sum(x[0, i] for i in range(numNode) if matrix[0][i] != 0) -
        sum(x[i, 0] for i in range(numNode) if matrix[i][0] != 0)) == 1)
    solver.Add((sum(x[numNode - 1, i] for i in range(numNode) if matrix[numNode - 1][i] != 0) -
        sum(x[i, numNode - 1] for i in range(numNode) if matrix[i][numNode - 1] != 0)) == -1)

    # RB: nếu đi vào từ i thì phải đi ra khoi i
    # (1,1) (0,0)
    for i in range(1, numNode - 1):
        solver.Add((sum(x[i, j] for j in range(numNode) if matrix[i][j] != 0) -
            sum(x[j, i] for j in range(numNode) if matrix[j][i] != 0)) == 0)


def MLEDP(numNode,matrix):
    solver = pywraplp.Solver.CreateSolver('SAT')

    #Bien x[i,j] = 1  có đường đi từ i đến j (path 0)
    #Biến y[i,j] = 1  có đường đi từ i đến j (path 1)
    x = {}
    y = {}
    for i in range(numNode):
        for j in range(numNode):
            if matrix[i][j] != 0:
                x[i, j] = solver.BoolVar(f'x[{i},{j}]')
                y[i, j] = solver.BoolVar(f'y[{i},{j}]')

    #Hàm mục tiêu:
    solver.Minimize(sum(x[i, j] * matrix[i][j] for i in range(numNode) for j in range(numNode) if matrix[i][j]!= 0) +
                    sum(y[i, j] * matrix[i][j] for i in range(numNode) for j in range(numNode) if matrix[i][j]!= 0))

    #Cân bằng luồng
    Balance(solver, x, numNode, matrix)
    Balance(solver, y, numNode, matrix)

    #RB: hai đường không có cạnh chung
    for i in range(numNode):
        for j in range(numNode):
            if matrix[i][j] != 0:
                solver.Add(x[i, j] + y[i, j] <= 1)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
    else:
        print('NOT_FEASIBLE')


if __name__ == '__main__':
    numNode, numEdge = map(int,input().split())
    matrix = [[0 for _ in range(numNode)] for _ in range(numNode)]
    for i in range(numEdge):
        u, v, w = map(int, input().split())
        matrix[u - 1][v - 1] = w

    MLEDP(numNode,matrix)