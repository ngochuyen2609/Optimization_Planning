from ortools.linear_solver import pywraplp

def main():
    soThanhPho = int(input())
    c=[]
    for i in range(soThanhPho):
        row = list(map(int, input().split()))
        c.append(row)

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Khai báo biến : x[i,j] = {0,1}
    x = {}
    for i in range(soThanhPho):
        for j in range(soThanhPho):
            if i != j and c[i][j] != 0:
                x[i,j] = solver.IntVar(0, 1, f'x[{i},{j}]')
            else:
                x[i, j] = solver.IntVar(0, 0, f'x[{i},{j}]')

    t = {}
    for i in range(soThanhPho):
        t[i] = solver.IntVar(0, soThanhPho - 1, f't[{i}]')

    # Hàm mục tiêu : x[i,j] * c[i][j] min
    solver.Minimize(solver.Sum(x[i,j] * c[i][j] for i in range(soThanhPho) for j in range(soThanhPho)))

    # Ràng buộc: mỗi thành phố chỉ được đi qua 1 lần
    for i in range(soThanhPho):
        solver.Add(solver.Sum(x[i,j] for j in range(soThanhPho)) == 1)
        solver.Add(solver.Sum(x[j, i] for j in range(soThanhPho)) == 1)

    # Ràng buộc: tránh chu trình con
    for i in range(1, soThanhPho):
        for j in range(soThanhPho):
            if i != j:
                solver.Add(t[i] - t[j] + soThanhPho * x[i, j] <= soThanhPho - 1)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(soThanhPho)
        print(int(solver.Objective().Value()))
        result = []
        curr = 0
        result.append(curr)
        while len(result) < soThanhPho:
            for next in range(soThanhPho):
                if x[curr, next].solution_value() > 0.5:
                    result.append(next)
                    curr = next
                    break
        for i in range(len(result) ):
            print(f"{result[i] + 1}", end=" ")
    else:
        print(-1)

if __name__ == '__main__':
    main()