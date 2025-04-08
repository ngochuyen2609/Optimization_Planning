TSP - Large Scale (Heuristic)
Mô tả
There are n cities 1, 2, ..., n. The travel distance from city i to city j is c(i,j), for i,j = 1, 2, ..., n.  A person wants to find a closed tour that visits each city exactly once (excelt the starting city). Find the itinerary for that person so that the total travel distance is minimal.
A solution is represented by a sequence x
Input
Line 1: a positive integer n (1 <= n <= 1000)
Line i+1 (i = 1, . . ., n): contains the ith row of the distance matrix x (elements are separated by a SPACE character)
Output
Line 1: write n
Line 2: write the sequence of points x

Thuật toán : HillClimbing

----------------------------------------------------------------------------------------------------------------------
TSP large solved exactly
Input
Line 1: a positive integer n (1 <= n <= 200)
Line i+1 (i = 1, . . ., n): contains the ith row of the distance matrix x (elements are separated by a SPACE character)

Output
Line 1: write the value n
Line 2: write x[1], x[2], . . ., x[n] (after each element, there is a SPACE character)

Thuật toán : SCIP ( có thể dùng lazyconstraint)
Thuật toán : SCIP2 ( n nhỏ hơn thuật toán 1 do nhiều thêm 1 biến )
-----------------------------------------------------------------------------------------------------------------------