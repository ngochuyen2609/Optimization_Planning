import heapq
import random
import time
import statistics


def check(path, passengers, places):
    n = len(path)
    positions = [-1] * (2 * passengers + 1)
    for idx, point in enumerate(path):
        positions[point] = idx

    for i in range(1, passengers + 1):
        if positions[i] > positions[i + passengers]:
            return False

    current_passengers = 0
    for point in path:
        if 1 <= point <= passengers:
            current_passengers += 1
        elif passengers + 1 <= point <= 2 * passengers:
            current_passengers -= 1
        if current_passengers > places or current_passengers < 0:
            return False

    return True

def calc_path(path, passengers, places, capacity):
    if not check(path, passengers, places):
        return float('inf')

    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += capacity[path[i]][path[i + 1]]
    return total_cost

'''
chiến lược khởi tạo:(tham lam)
    Nếu còn đón được(còn ghế, còn khách chưa đón) đón khách (trong k khách gần nhất) so với điểm hiện tại
    Không còn đón đươc(ầy xe hoặc đã đón hết khách) trả khách (trong k khách gần nhất) so với điểm hiện tại
    * là k khách gần nhất không phải khách gần nhất để tiện khởi tạo lại khi gặp cực trị địa phương
    * dùng greedy không phải random để đảm bảo lời giải khởi tạo đủ tốt(tránh mất thời gian)
'''
def init_solution(passengers, places, capacity, k=3):
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
            # Trả khách nếu xe đầy hoặc không còn khách để đón
            for p in onboard:
                drop = p + passengers
                if not visited[drop]:
                    candidates.append((capacity[current][drop], drop))

        elif not onboard:
            # Nếu xe rỗng → bắt buộc phải đón
            for p in remaining_pickups:
                if not visited[p]:
                    candidates.append((capacity[current][p], p))

        else:
            # Nếu còn ghế và còn cả khách và người để trả → ưu tiên điểm gần nhất bất kể đón hay trả
            for p in onboard:
                drop = p + passengers
                if not visited[drop]:
                    candidates.append((capacity[current][drop], drop))
            for p in remaining_pickups:
                if not visited[p]:
                    candidates.append((capacity[current][p], p))

        if not candidates:
            break

        # Sắp xếp và lấy top-k điểm gần nhất
        candidates.sort()
        top_k = candidates[:k] if len(candidates) >= k else candidates
        _, next_point = random.choice(top_k)

        path.append(next_point)
        visited[next_point] = True

        if 1 <= next_point <= passengers:
            onboard.add(next_point)
            remaining_pickups.remove(next_point)
        elif passengers + 1 <= next_point <= 2 * passengers:
            onboard.remove(next_point - passengers)
            remaining_dropoffs.remove(next_point)

        current = next_point

    path.append(0)
    if not check(path, passengers, places):
        return None
    return path


def get_neighbors(path, passengers, places, num_neighbors=50):
    neighbors = []
    sub_path = path[1:-1]
    sub_n = len(sub_path)

    attempts = 0
    max_attempts = num_neighbors * 5
    while len(neighbors) < num_neighbors and attempts < max_attempts:
        transformation = random.choice(['swap', 'reverse', 'insert'])
        neighbor = sub_path[:]

        # đảo đỉnh
        if transformation == 'swap':
            i = random.randint(0, sub_n - 1)
            j = random.randint(0, sub_n - 1)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        # đảo ngược đoạn
        elif transformation == 'reverse':
            i = random.randint(0, sub_n - 2)
            j = random.randint(i + 1, sub_n - 1)
            neighbor[i:j+1] = neighbor[i:j+1][::-1]

        # chèn đỉnh
        else:
            i = random.randint(0, sub_n - 1)
            point = neighbor.pop(i)
            j = random.randint(0, sub_n - 2)
            neighbor.insert(j, point)

        full_neighbor = [0] + neighbor + [0]
        if check(full_neighbor, passengers, places):
            neighbors.append(full_neighbor)

        attempts += 1

    return neighbors


'''
Chiến lược leo đồi:
    Ban đầu khởi tạo lời giải đủ tốt theo greedy nhưng vẫn có tính ngẫu nhiên:
        Khởi tạo 5 lời giải và chọn lời giải tốt nhất
    Leo đồi:
        Tạo hàng xóm bằng các phép biến đổi (hoán đổi, đảo đoạn, chèn điểm), 
        Chọn lộ trình có chi phí thấp nhất để cải thiện.
        Nếu bị kẹt ở cực trị địa phương, tạo lại lộ trình mới 
'''
def hill_climbing_CBUS(passengers, places, capacity):
    TIME_LIMIT = 250
    start_time = time.time()

    best_path = None
    best_cost = float('inf')

    # tạo nhiều lời giải ban đầu và chọn giải pháp tốt nhất
    initial_paths = []
    for _ in range(5):
        path = init_solution(passengers, places, capacity)
        if path is not None:
            cost = calc_path(path, passengers, places, capacity)
            if cost < float('inf'):
                initial_paths.append((path, cost))
    if not initial_paths:
        print(-1)
        return
    current_path, current_cost = min(initial_paths, key=lambda x: x[1])
    if current_cost < best_cost:
        best_cost = current_cost
        best_path = current_path

    #Hill climbing
    stagnation_count = 0
    max_stagnation = 100

    while time.time() - start_time <= TIME_LIMIT:
        neighbors = get_neighbors(current_path, passengers, places, num_neighbors=50)
        best_neighbor = None
        best_neighbor_cost = current_cost

        for neighbor in neighbors:
            cost = calc_path(neighbor, passengers, places, capacity)
            if cost < best_neighbor_cost:
                best_neighbor_cost = cost
                best_neighbor = neighbor

        if best_neighbor is None:
            stagnation_count += 1
        else:
            current_path = best_neighbor
            current_cost = best_neighbor_cost
            stagnation_count = 0
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = current_path

        # Random restart nếu bị kẹt quá lâu
        if stagnation_count >= max_stagnation:
            for _ in range(5):
                new_path = init_solution(passengers, places, capacity)
                if new_path is None:
                    continue
                new_cost = calc_path(new_path, passengers, places, capacity)
                if new_cost < float('inf'):
                    current_path = new_path
                    current_cost = new_cost
                    stagnation_count = 0
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_path = current_path
                    break
            else:
                stagnation_count = 0  # Reset để tránh lặp vô hạn

    if best_cost == float('inf') or best_path is None:
        print(-1)
    else:
        print(int(best_cost))
        print(passengers)
        for i in range(1, len(best_path) - 1):
            print(f"{best_path[i]}", end=" ")
            print()

    duration = time.time() - start_time
    return best_cost, best_path, duration

if __name__ == '__main__':
    passengers, places = map(int, input().split())
    capacity = [list(map(int, input().split())) for _ in range(2 * passengers + 1)]
    hill_climbing_CBUS(passengers, places, capacity)

    results = []
    times = []

    for _ in range(3):
        cost, path, elapsed = hill_climbing_CBUS(passengers, places, capacity)
        results.append(cost)
        times.append(elapsed)

    if all(cost == float('inf') for cost in results):
        print(-1)
    else:
        valid_results = [c for c in results if c != float('inf')]
        print(f"min: {min(valid_results)}")
        print(f"max: {max(valid_results)}")
        print(f"avg: {sum(valid_results) / len(valid_results):.2f}")
        print(f"std: {statistics.stdev(valid_results):.2f}" if len(valid_results) > 1 else "std: N/A")
        print(f"tavg: {sum(times) / len(times):.2f}s")