soBien, soRangBuoc = map(int, input().split())
# bai toan QHTT (bien la so thuc)
# <=
matrix1 = list(map(int, input().split()))

matrix2 = []
for _ in range(soRangBuoc + 1):
    row = [0] * (soBien + soRangBuoc + 2)
    matrix2.append(row)

for i in range(soBien):
    matrix2[soRangBuoc][i] = -matrix1[i]

for i in range(soRangBuoc):
    row = list(map(int, input().split()))
    matrix2[i][soBien + i] = 1
    for j in range(soBien):
        matrix2[i][j] = row[j]

b_values = list(map(int, input().split()))  
for i in range(soRangBuoc):
    matrix2[i][soBien + soRangBuoc + 1] = b_values[i]

matrix2[soRangBuoc][soBien + soRangBuoc] = 1

while True:
    col = -1
    minam = 0
    for i in range(soBien + soRangBuoc):
        if matrix2[soRangBuoc][i] < minam and matrix2[soRangBuoc][i] < 0:
            col = i
            minam = matrix2[soRangBuoc][i]

    if col == -1:
        break

    row = -1
    min_ratio = float('inf')
    for i in range(soRangBuoc):
        if matrix2[i][col] > 0:
            ratio = matrix2[i][soBien + soRangBuoc + 1] / matrix2[i][col]
            if ratio < min_ratio:
                min_ratio = ratio
                row = i

    if row == -1:
        print("UNBOUNDED")
        exit()

    pivot = matrix2[row][col]
    for j in range(soBien + soRangBuoc + 2):
        matrix2[row][j] /= pivot

    for i in range(soRangBuoc + 1):
        if i != row:
            factor = matrix2[i][col]
            for j in range(soBien + soRangBuoc + 2):
                matrix2[i][j] -= factor * matrix2[row][j]

# print(matrix2[soRangBuoc][soBien + soRangBuoc + 1])
print(soBien)

for i in range(soBien):
    if(matrix2[soRangBuoc ][i] == 0):
        for j in range(soRangBuoc):
            if(matrix2[j][i] == 1):
                print(matrix2[j][soBien+ soRangBuoc + 1],end=" ")
    else: 
        print(0)
# for row in matrix2:
#     print("  ".join(map(str, row)))
