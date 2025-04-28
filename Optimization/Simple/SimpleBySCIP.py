from ortools.linear_solver import pywraplp

def main():
    soBien, soRangBuoc = map(int, input().split())
    c = list(map(int, input().split()))
    A =[]
    for i in range(soRangBuoc):
        row = list(map(int, input().split()))
        A.append(row)
    b = list(map(int, input().split()))

    solver = (pywraplp.Solver.CreateSolver('SCIP'))

    # khởi tạo biến:
    x = {}
    for _ in range(soBien):
        x[_] = solver.NumVar(0, solver.infinity(), f'x[{_}]' )

    # Hàm mục tiêu:
    solver.Maximize(solver.Sum(c[i] * x[i] for i in range(soBien)))

    # Ràng buộc:
    for i in range(soRangBuoc):
        solver.Add(solver.Sum(A[i][_]*x[_] for _ in range(soBien)) <= b[i])

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(soBien)
        for _ in range(soBien):
            print(f"{x[_].solution_value():.1f}", end=' ')
    else:
        print('UNBOUNDED')

if __name__ == '__main__':
    main()