from ortools.linear_solver import pywraplp

def BCA(soGiaoVien, soMonHoc, monHocs, soConflict, conFlicts):
    solver = pywraplp.Solver.CreateSolver('SAT')

    # Khai báo biến x[i, j] = 1 thì môn i giao cho giáo viên j
    x = {}
    for gv in range(soGiaoVien):
        mark = [False for _ in range(soMonHoc)]
        for i in monHocs[gv]:
            mark[i - 1] = True

        for i in range(soMonHoc):
            if  mark[i] == True :
                x[i, gv] = solver.IntVar(0, 1, f'x[{i},{gv}]')
            else:
                x[i, gv] = solver.IntVar(0, 0, f'x[{i},{gv}]')

    # Khai báo biến y: số môn tối đa mà 1 giáo viên có thể dạy
    y = solver.IntVar(0, soMonHoc, f'y')

    # Hàm mục tiêu: minimize y
    solver.Minimize(y)

    #RB: mỗi môn chỉ được do 1 giáo viên dạy
    for i in range(soMonHoc):
        solver.Add(sum(x[i,j] for j in range(soGiaoVien)) == 1)

    #RB: y là số lượng môn học tối đa gv i được dạy
    for gv in range(soGiaoVien):
        solver.Add(sum(x[i, gv] for i in range(soMonHoc)) <= y)

    #RB: giáo viên không được dạy môn conflict
    for gv in range(soGiaoVien):
        for i, j in conFlicts:
            solver.Add(x[i - 1, gv] + x[j - 1, gv] <= 1)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(int( y.solution_value() ))
    else:
        print(-1)


if __name__ == '__main__':
    soGiaoVien, soMonHoc = map(int,input().split())
    monHocs = []
    for i in range(soGiaoVien):
        row = list(map(int,input().split()))
        monHocs.append(set( row [1:] ))
    soConflict = int(input())
    conFlicts = []
    for i in range(soConflict):
        conFlicts.append(list(map(int,input().split())))

    BCA(soGiaoVien, soMonHoc, monHocs, soConflict, conFlicts)
