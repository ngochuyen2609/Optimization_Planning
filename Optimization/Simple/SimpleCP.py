from ortools.sat.python import cp_model

class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.result_val = {i : set() for i in range(len(x))}

    def on_solution_callback(self):
        for i, val in enumerate(self.x):
            self.result_val[i].add(self.Value(val))

def main():
    soBien = int(input())
    domain = {}
    for i in range(soBien):
        row = list(map(int, input().split()))
        domain[i] = row[1:]
    soRangBuoc = int(input())
    constraints = []
    for i in range(soRangBuoc):
        row = list(map(int, input().split()))
        constraints.append(row)

    model = cp_model.CpModel()

    #Khai báo biến
    x = {}
    for i in range(soBien):
        x[i] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain[i]), f'x[{i}]')

    #Khai báo ràng buộc
    for a,b,c in constraints:
        model.Add(x[a - 1] <= x[b - 1] + c)

    solver = cp_model.CpSolver()
    collector = SolutionCollector(list(x.values()))
    status = solver.SearchForAllSolutions(model,collector)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(soBien):
            result = sorted(collector.result_val[i])
            print(len(result), ' '.join(map(str,result)))

        exit(0)
    else:
        print('FAIL')

if __name__ == '__main__':
    main()