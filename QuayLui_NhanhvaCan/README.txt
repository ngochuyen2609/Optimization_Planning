Thuật toán : Backtracking

CBUS:
There are n passengers 1, 2, …, n. The passenger i want to travel from point i to point i + n (i = 1,2,…,n). There is a bus located at point 0 and has k places for transporting the passengers (it means at any time, there are at most k passengers on the bus). You are given the distance matrix c in which c(i,j) is the traveling distance from point i to point j (i, j = 0,1,…, 2n). Compute the shortest route for the bus, serving n passengers and coming back to point 0.
Input
    Line 1 contains n and k (1≤n≤11,1≤k≤10)
    Line i+1 (i=1,2,…,2n+1) contains the (i−1)th line of the matrix c (rows and columns are indexed from 0,1,2,..,2n).
Output
    Unique line contains the length of the shortest route.


TSP small size
There are n cities 1, 2, ..., n. The travel distance from city i to city j is c(i,j), for i,j = 1, 2, ..., n.  A person departs from city 1, visits each city 2, 3, ..., n exactly once and comes back to city 1. Find the itinerary for that person so that the total travel distance is minimal.
Input
    Line 1: a positive integer n (1 <= n <= 20)
    Line i+1 (i = 1, . . ., n): contains the ith row of the distance matrix x (elements are separated by a SPACE character)
Output
    Write the total travel distance of the optimal itinerary found.

Description
A fleet of K identical trucks having capacity Q need to be scheduled to delivery pepsi packages from a central depot 0 to clients 1,2,…,n. 
Each client i requests d[i] packages. The distance from location i to location j is c[i,j], 0≤i,j≤n.
A delivery solution is a set of routes: each truck is associated with a route, starting from depot,
visiting some clients and returning to the depot for deliverying requested pepsi packages such that:
Each client is visited exactly by one route
Total number of packages requested by clients of each truck cannot exceed its capacity
Goal
Find a solution having minimal total travel distance
Note that:
There might be the case that a truck does not visit any client (empty route)
The orders of clients in a route is important, e.g., routes 0 -> 1 -> 2 -> 3 -> 0 and 0 -> 3-> 2 -> 1 -> 0 are different.
Input
    Line 1: n,K,Q (2≤n≤12,1≤K≤5,1≤Q≤50)
    Line 2: d[1],...,d[n](1≤d[i]≤10)
    Line i+3 (i=0,…,n): the ith row of the distance matrix c (1≤c[i,j]≤30)
Output
    Minimal total travel distance