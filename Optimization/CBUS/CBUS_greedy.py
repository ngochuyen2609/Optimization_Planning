import heapq

def greedy_route(passengers, places, capacity):
    n = 2 * passengers + 1
    visited = [False] * n
    onboard = set()
    path = [0]
    current = 0
    remaining_pickups = set(range(1, passengers + 1))
    remaining_dropoffs = set(range(passengers + 1, n))

    while remaining_pickups or remaining_dropoffs:
        candidates = []

        if len(onboard) >= places or not remaining_pickups:
            # Ưu tiên trả khách
            for p in onboard:
                drop = p + passengers
                if not visited[drop]:
                    heapq.heappush(candidates, (capacity[current][drop], drop))
        else:
            # Ưu tiên đón khách
            for p in remaining_pickups:
                heapq.heappush(candidates, (capacity[current][p], p))

        if not candidates:
            break

        _, next_point = heapq.heappop(candidates)
        path.append(next_point)
        visited[next_point] = True

        if 1 <= next_point <= passengers:
            onboard.add(next_point)
            remaining_pickups.remove(next_point)
        else:
            onboard.remove(next_point - passengers)
            remaining_dropoffs.remove(next_point)

        current = next_point

    path.append(0)

    print(passengers)
    print(" ".join(map(str, path[1:-1])))

if __name__ == '__main__':
    import sys
    passengers, places = map(int, input().split())
    capacity = [list(map(int, sys.stdin.readline().split())) for _ in range(2 * passengers + 1)]
    greedy_route(passengers, places, capacity)
