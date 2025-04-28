from ortools.sat.python import cp_model

def CBUS(passengers, places, capacity):
    model = cp_model.CpModel()

    n = passengers * 2 + 1

    # Khởi tạo biến x[i,j]:
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

    # Khởi tạo biến t[i]: Thứ tự ghé thăm của điểm i
    t = {}
    for i in range(n):
        t[i] = model.NewIntVar(0, n - 1, f't[{i}]')

    # Khởi tạo biến q[i]: Số khách trên xe sau khi ghé thăm điểm i
    q = {}
    for i in range(n):
        q[i] = model.NewIntVar(0, places, f'q[{i}]')

    # Hàm mục tiêu:
    model.Minimize(sum(x[i,j] * capacity[i][j] for i in range(n) for j in range(n) if i != j))

    # RB: mỗi điểm chỉ đi qua 1 lần
    for i in range(n):
        model.Add(sum(x[i, j] for j in range(n) if i != j) == 1)
        model.Add(sum(x[j, i] for j in range(n) if i != j) == 1)

    # RB: Đón khách trước trả khách
    for i in range(1, passengers + 1):
        model.Add(t[i] + 1 <= t[i + passengers])

    # RB: Số khách trên xe không vượt quá places
    model.Add(q[0] == 0)
    for i in range(n):
        for j in range(n):
            if i != j:
                delta = 0
                if 1 <= j <= passengers:
                    delta = 1
                elif passengers + 1 <= j <= 2 * passengers:
                    delta = -1
                model.Add(q[j] == q[i] + delta).OnlyEnforceIf(x[i, j])

    # RB: Tránh chu trình con (MTZ)
    for i in range(1, n):
        for j in range(n):
            if i != j:
                model.Add(t[i] - t[j] + n * x[i, j] <= n - 1)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(passengers)
        result = [0]
        curr = 0
        while len(result) < n:
            for next in range(n):
                if (curr, next) in x and solver.Value(x[curr, next]) == 1:
                    result.append(next)
                    curr = next
                    break

        for i in range(1,len(result)):
            print(f"{result[i]}", end=" ")
    else:
        print(-1)

if __name__ == '__main__':
    passengers, places = map(int, input().split())
    capacity = []
    for i in range(passengers * 2 + 1):
        capacity.append(list(map(float, input().split())))

    CBUS(passengers, places, capacity)