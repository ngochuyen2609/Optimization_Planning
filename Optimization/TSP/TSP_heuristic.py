import time

def cost(tour, dis):
    total = 0
    n = len(tour)
    for i in range(n - 1):
        total += dis[tour[i]][tour[i + 1]]
    total += dis[tour[-1]][tour[0]]
    return total

def hillClimbing(tour, dist):
    n = len(tour)
    best_cost = cost(tour, dist)

    for i in range(n - 1):
        for j in range(i + 2, n): # đảo 2 đỉnh liền kề không có tác dụng
            if j == n - 1 and i == 0:
                continue
            new_tour = tour[:]
            new_tour[i + 1:j + 1] = reversed(new_tour[i + 1:j + 1])
            new_cost = cost(new_tour, dist)
            if new_cost < best_cost:
                tour[:] = new_tour
                return True
    return False

def nearest_node(dist, visited, current, n):
    min_dis = float('inf')
    next_city = -1
    for j in range(n):
        if not visited[j] and dist[current][j] < min_dis:
            min_dis = dist[current][j]
            next_city = j
    return next_city

if __name__ == '__main__':
    n = int(input())
    distance = [list(map(int, input().split())) for _ in range(n)]

    best_tours = []
    # xây dựng
    for start in range(n):
        visited = [False] * n
        visited[start] = True
        tour = [start]
        current = start
        for _ in range(n - 1):
            next_city = nearest_node(distance, visited, current, n)
            tour.append(next_city)
            visited[next_city] = True
            current = next_city
        best_tours.append(tour)

    #cải tạo : đảo đỉnh
    start_time = time.time()
    time_limit = 120
    res_tour = None

    for tour in best_tours:
        if time.time() - start_time >= time_limit:
            break
        temp = True
        while temp:
            if time.time() - start_time >= time_limit:
                break
            temp = hillClimbing(tour, distance)
        if res_tour is None or cost(tour, distance) < cost(res_tour, distance):
            res_tour = tour[:]

    print(n)
    print(" ".join(str(i + 1) for i in res_tour))