from ortools.linear_solver import pywraplp

def CBUS(passengers, places, capacity):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    n = passengers * 2 + 1

    #Khai báo biến x[i,j]
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j and capacity[i][j] != 0:
                x[i, j] = solver.IntVar(0, 1, f'x[{i,j}]')
            else:
                x[i, j] = solver.IntVar(0, 0, f'x[{i, j}]')

    # Khai báo biến: t[i] thời điểm đến i
    t = {}
    for i in range(n):
        t[i] = solver.IntVar(0, n - 1, f't[{i}]')

    # Khai báo biến: q[i] số khách trên xe tại điểm i
    q = {}
    for i in range(n):
        q[i] = solver.IntVar(0, places, f'q[{i}]')

    #Hàm mục tiêu
    solver.Minimize(solver.Sum(x[i,j] * capacity[i][j] for i in range(n) for j in range(n) ))

    #RB: mỗi điểm chỉ đi qua 1 lần
    for i in range(n):
        solver.Add(solver.Sum(x[i, j] for j in range(n)) == 1)
        solver.Add(solver.Sum(x[j, i] for j in range(n)) == 1)

    #RB: đón trước khi trả
    for i in range(1, passengers + 1):
        solver.Add(t[i] + 1 <= t[i + passengers])

    #RB: không chở quá sso người trên xe
    solver.Add(q[0] == 0)
    for i in range(n):
        for j in range(n):
            if i != j:
                delta = 0
                if 1 <= j <= passengers:
                    delta = 1
                elif passengers + 1 <= j <= 2 * passengers:
                    delta = -1
                solver.Add(q[j] >= q[i] + delta - (1 - x[i,j]) * n)
                solver.Add(q[j] <= q[i] + delta + (1 - x[i, j]) * n)

    #RB: tránh chu trình con t[j] == t[i] + 1 nếu x[i, j] ==1
    for i in range(1, n):
        for j in range(n):
            if i != j:
                solver.Add(t[i] - t[j] + n * x[i, j] <= n - 1)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
        for i in range(n):
            print(f'{t[i].solution_value()}', end=" ")
        print()
        print(passengers)
        result = []
        curr = 0
        while len(result) < 2 * passengers:
            for next in range(n):
                if x[curr, next].solution_value() == 1:
                    result.append(next)
                    curr = next
                    break
        for i in result:
            print(f'{i}',end=" ")
    else:
        print(-1)

if __name__ == "__main__":
    passengers, places = map(int, input().split())
    capacity = []
    for _ in range(passengers * 2 + 1):
        capacity.append(list(map(int, input().split())))

    CBUS(passengers, places, capacity)