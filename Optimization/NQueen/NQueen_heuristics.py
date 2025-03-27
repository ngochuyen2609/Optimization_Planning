import random
import time

def generated_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def check_conflict(row, col,row_conflict, cross1_conflict, cross2_conflict, n):
    return (row_conflict[row] > 1 or
            cross1_conflict[row + col] > 1 or
            cross2_conflict[row - col + n - 1] > 1)

def count_conflict(n, board):
    row_conflict = [0] * n
    cross1_conflict = [0] * (2 * n - 1)
    cross2_conflict = [0] * (2 * n - 1)
    conflicts = set()

    for col in range(n):
        row = board[col]
        row_conflict[row] += 1
        cross1_conflict[row + col] +=1
        cross2_conflict[row - col + n -1] += 1

        if check_conflict(row, col,row_conflict, cross1_conflict, cross2_conflict, n):
            conflicts.add(col)

    return row_conflict, cross1_conflict, cross2_conflict, conflicts

def get_conflicted_column(conflicts):
    if conflicts:
        return random.choice(list(conflicts))
    return None

def move_queen(n, board, col, row_conflict, cross1_conflict, cross2_conflict, conflicts):
    original_row = board[col]
    min_conflict = n
    best_rows = []

    for r in range(n):
        if r == original_row:
            continue

        # Tính toán tổng xung đột nếu di chuyển quân hậu đến r.
        new_conflict = (row_conflict[r] +
                        cross1_conflict[r + col] +
                        cross2_conflict[r - col + n - 1])

        if new_conflict < min_conflict:
            min_conflict = new_conflict
            best_rows = [r]
        elif new_conflict == min_conflict:
            best_rows.append(r)

    if best_rows:
        new_row = random.choice(best_rows)

        row_conflict[original_row] -= 1
        cross1_conflict[original_row + col] -= 1
        cross2_conflict[original_row - col + n - 1] -= 1
        board[col] = new_row
        row_conflict[new_row] += 1
        cross1_conflict[new_row + col] += 1
        cross2_conflict[new_row - col + n - 1] += 1

        if check_conflict(original_row, col, row_conflict, cross1_conflict, cross2_conflict, n):
            conflicts.add(col)
        else:
            conflicts.discard(col)

def solve_n_queens(n, max_time=120):
    board = generated_board(n)
    row_conflict, cross1_conflict, cross2_conflict, conflicts = count_conflict(n, board)

    start_time = time.time()
    while conflicts:
        if time.time() - start_time > max_time:
            return None

        col = get_conflicted_column(conflicts)
        if col is None:
            return board

        move_queen(n, board, col, row_conflict, cross1_conflict, cross2_conflict, conflicts)

    return board

if __name__ == '__main__':
    n = int(input())
    solution = solve_n_queens(n)

    print(len(solution))
    print(' '.join(str(x + 1) for x in solution))
