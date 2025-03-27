from ortools.sat.python import cp_model
def sol():
    # n number of courses
    # p number of semesters
    n, p = map(int, input().split())
    credits = list(map(int, input().split()))
    # alpha <= number of courses in a semester <= beta
    # lam <= number of credit in a semester <= gam
    alpha, beta, lam, gam = map(int, input().split())
    # m number of prerequisites
    m = int(input())
    # prequisites
    DKTQ = []
    for _ in range(m):
        DKTQ.append(list(map(int, input().split())))

    model = cp_model.CpModel()

    # Khai báo biến : x[p,i] môn i giao vào kỳ p
    x = {}
    for sem in range(p):
        for course in range(n):
            x[sem,course] = model.NewIntVar(0, 1, f'x[{sem},{course}]')

    #RB1: 1 môn chỉ mở vào 1 kỳ
    for course in range(n):
        model.Add(sum(x[sem, course] for sem in range(p) ) == 1)
    #RB2, RB3:
    for sem in range(p):
        course_semester = sum(x[sem, course] for course in range(n))
        model.Add(course_semester >= alpha)
        model.Add(course_semester <= beta)
        credit_semester = sum(x[sem, course] * credits[course] for course in range(n))
        model.Add(credit_semester >= lam)
        model.Add(credit_semester <= gam)
    #RB4: Điều kiện tiên quyết
    for (first, second) in DKTQ:
        for sem in range(p):
            model.Add(x[sem, second] <=  sum(x[front_sem, first] for front_sem in range(sem)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for sem in range(p):
            print(sem + 1, end=' : ')
            for course in range(n):
                if (solver.Value(x[sem,course]) == 1):
                    print(course, end=' ')
            print()
    else:
        print('FAIL')

if __name__ == '__main__':
    sol()