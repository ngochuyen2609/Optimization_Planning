from ortools.linear_solver import pywraplp

def main():
    # Tạo một solver LP (Linear Programming) với phương pháp GLOP (Google's Linear Optimizer)
    solver = pywraplp.Solver.CreateSolver('GLOP')

    if not solver:
        print('GLOP solver không có sẵn!')
        return

    # Khai báo các biến quyết định x và y
    x = solver.IntVar(0.0, solver.infinity(), 'x')  # Biến x, >= 0
    y = solver.IntVar(0.0, solver.infinity(), 'y')  # Biến y, >= 0

    print(f'Variable x: {x}, y: {y}')

    # Thêm các ràng buộc
    solver.Add(x + y <= 4)  # ràng buộc x + y <= 4
    solver.Add(2 * x + y <= 5)  # ràng buộc 2x + y <= 5

    # Đặt hàm mục tiêu: tối đa hoá z = 3x + 2y
    solver.Maximize(3 * x + 2 * y)

    # Giải bài toán
    status = solver.Solve()

    # Kiểm tra kết quả và in ra
    if status == pywraplp.Solver.OPTIMAL:
        print(f'Optimal solution found: x = {x.solution_value()}, y = {y.solution_value()}')
        print(f'Optimal objective value: {solver.Objective().Value()}')
    else:
        print('No optimal solution found.')

if __name__ == '__main__':
    main()
