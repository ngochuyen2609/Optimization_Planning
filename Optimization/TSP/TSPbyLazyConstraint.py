from ortools.linear_solver import pywraplp

def find_subtour(soThanhPho, adj):
    cycles = []
    visited = [False] * soThanhPho
    cyc = []

    def find_cycle(curr):
        cycle = [curr]
        visited[curr] = True
        while True:
            next_node = adj[curr]
            if visited[next_node]:
                return cycle
            cycle.append(next_node)
            visited[next_node] = True
            curr = next_node

    for start in range(soThanhPho):
        if not visited[start]:
            cycle = find_cycle(start)
            cycles.append(cycle)

    return cycles

def main():
    soThanhPho = int(input())
    c = []
    for i in range(soThanhPho):
        row = list(map(int, input().split()))
        c.append(row)

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Khởi tạo biến x[i,j] = 1 nếu có chuyến đi từ i đến j
    x = {}
    for i in range(soThanhPho):
        for j in range(soThanhPho):
            if i != j and c[i][j] != 0:
                x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')
            else:
                x[i, j] = solver.IntVar(0, 0, f'x[{i},{j}]')

    # Hàm mục tiêu: minimize tổng chi phí
    solver.Minimize(solver.Sum(x[i,j] * c[i][j] for i in range(soThanhPho) for j in range(soThanhPho)))

    # Ràng buộc: mỗi thành phố chỉ được đi qua 1 lần
    for i in range(soThanhPho):
        solver.Add(solver.Sum(x[i, j] for j in range(soThanhPho) if i != j) == 1)
        solver.Add(solver.Sum(x[j, i] for j in range(soThanhPho) if i != j) == 1)

    # lazy constraints
    while True:
        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL:
            break

        adj = [-1] * soThanhPho
        for i in range(soThanhPho):
            for j in range(soThanhPho):
                if x[i, j].solution_value() == 1:
                    adj[i] = j

        cycles = find_subtour(soThanhPho, adj)

        if len(cycles) == 1:
            print(soThanhPho)
            for i in range(soThanhPho):
                print(cycles[0][i] + 1, end=' ')
            break
        else:
            for cycle in cycles:
                if len(cycle) > 1:
                    solver.Add(solver.Sum(x[i, j] for i in cycle for j in cycle) <= len(cycle) - 1)

if __name__ == "__main__":
    main()