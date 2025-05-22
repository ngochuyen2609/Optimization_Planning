from  ortools.sat.python import cp_model

numCourse = 9
numSemester = 4
## số tín chỉ
credit = [3, 2, 2, 1, 3, 3, 1, 2, 2]
##tổng số môn học >= a và <= b
# tổng số tín chỉ >= l và <= g
alpha = 2
beta = 4
lamda = 3
gamma = 7
condition = [(0, 1), (0, 2), (1, 3), (2, 5), (3, 6), (4, 7), (3,8)]

model = cp_model.CpModel()

#Biến x[i,j] = 1 môn i được phân vào kỳ j
x = {}
for i in range(numCourse):
    for j in range(numSemester):
        x[i, j] = model.NewBoolVar(f'x[{i},{j}]')

#RB: tổng tín chỉ
for hk in range(numSemester):
    model.Add(sum(x[i, hk] * credit[i] for i in range(numCourse)) <= beta)
    model.Add(sum(x[i, hk] * credit[i] for i in range(numCourse)) >= alpha)

#RB: tổng số môn
for hk in range(numSemester):
    model.Add(sum(x[i, hk] for i in range(numCourse)) <= lamda)
    model.Add(sum(x[i, hk] for i in range(numCourse)) >= gamma)

#RB: thỏa mãn đk tiên quyết
#sum(x[u, hkt]) >= x[v,hk]
# (1,1) (1,0) (0,0)
for u, v in condition:
    for hk in range(numSemester):
        model.Add(sum(x[u, hkt] for hkt in range(hk)) >= x[v, hk])

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    for i in range(numCourse):
        for hk in range(numSemester):
            if(solver.Value(x[i,hk]) == 1):
                print(hk + 1, end=' ')

else:
    print(-1)
