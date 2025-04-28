from ortools.linear_solver import pywraplp

def main():
    soGiaoVien, soMonHoc = map(int, input().split())
    giaoVien_MonHoc = []
    for i in range(soGiaoVien):
        row = list(map(int, input().split()))
        giaoVien_MonHoc.append(set(row[1:]))
    soConflict = int(input())
    conflict = {i: set() for i in range(soMonHoc)}
    for i in range(soConflict):
        i, j = map(int, input().split())
        conflict[i - 1].add(j - 1)
        conflict[j - 1].add(i - 1)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Không thể tạo bộ giải SCIP.")
        return None

    # Khai báo biến: x[i,j] = 0,1 : lớp i giao cho gv j || y là lấy max số môn học
    x = {}
    for gv in range(soGiaoVien):
        # Khởi tạo mảng đánh dấu môn học mà gv có thể dạy
        mark = [False for _ in range(soMonHoc)]
        for i in giaoVien_MonHoc[gv]:
            mark[i - 1] = True

        for i in range(soMonHoc):
            if mark[i]:
                x[i, gv] = solver.IntVar(0.0, 1.0, f'x[{i},{gv}]')
            else:  # Nếu không thể dạy, giá trị là 0
                x[i, gv] = solver.IntVar(0.0, 0.0, f'x[{i},{gv}]')

    y = solver.IntVar(0.0, solver.infinity(), 'y')  # Biến y cho số môn học tối đa của giáo viên

    # Hàm mục tiêu: minimize max số môn học của 1 giáo viên
    for gv in range(soGiaoVien):
        solver.Add(solver.Sum(x[i, gv] for i in range(soMonHoc)) <= y)
    solver.Minimize(y)

    # Ràng buộc: không được dạy môn xung đột
    for i in range(soMonHoc):
        for gv in range(soGiaoVien):
            for j in conflict[i]:
                solver.Add(x[i, gv] + x[j, gv] <= 1)

    # Ràng buộc: mỗi môn học phải được giao cho một giáo viên duy nhất
    for i in range(soMonHoc):
        solver.Add(solver.Sum(x[i, gv] for gv in range(soGiaoVien)) == 1)

    # Giải bài toán
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(int(y.solution_value()))  # In ra giá trị tối ưu của y
    else:
        print(-1)  # Nếu không tìm thấy lời giải tối ưu


if __name__ == '__main__':
    main()
