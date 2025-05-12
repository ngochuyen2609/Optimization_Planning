import heapq

def calc_path(path, passengers, places, capacity):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += capacity[path[i]][path[i + 1]]
    return total_cost

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
            # Trường hợp 1: xe đầy hoặc không còn ai để đón → chỉ trả
            for p in onboard:
                drop = p + passengers
                if not visited[drop]:
                    candidates.append((capacity[current][drop], drop))

        elif not onboard:
            # Trường hợp 2: xe không có ai → chỉ đón
            for p in remaining_pickups:
                if not visited[p]:
                    candidates.append((capacity[current][p], p))

        else:
            # Trường hợp 3: chọn điểm gần nhất (đón hoặc trả)
            for p in onboard:
                drop = p + passengers
                if not visited[drop]:
                    candidates.append((capacity[current][drop], drop))
            for p in remaining_pickups:
                if not visited[p]:
                    candidates.append((capacity[current][p], p))

        if not candidates:
            break

        # Chọn điểm gần nhất
        _, next_point = min(candidates)
        path.append(next_point)
        visited[next_point] = True

        if 1 <= next_point <= passengers:
            # Là điểm đón
            onboard.add(next_point)
            remaining_pickups.remove(next_point)
        elif passengers + 1 <= next_point <= 2 * passengers:
            # Là điểm trả
            onboard.remove(next_point - passengers)
            remaining_dropoffs.remove(next_point)

        current = next_point

    path.append(0)  # Quay về điểm xuất phát

    # print(calc_path(path, passengers, places, capacity))
    print(passengers)
    print(" ".join(map(str, path[1:-1])))

if __name__ == '__main__':
    import sys
    passengers, places = map(int, input().split())
    capacity = [list(map(int, sys.stdin.readline().split())) for _ in range(2 * passengers + 1)]
    greedy_route(passengers, places, capacity)
