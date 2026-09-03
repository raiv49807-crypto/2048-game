import random


SIZE = 4


def start_game():
    mat = [[0] * SIZE for _ in range(SIZE)]

    print("Commands are as follows:")
    print("'W' or 'w': Move Up")
    print("'S' or 's': Move Down")
    print("'A' or 'a': Move Left")
    print("'D' or 'd': Move Right")

    add_new_2(mat)
    add_new_2(mat)
    return mat


def find_empty(mat):
    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 0:
                return i, j
    return None, None


def add_new_2(mat):
    empty_cells = [
        (i, j)
        for i in range(SIZE)
        for j in range(SIZE)
        if mat[i][j] == 0
    ]

    if empty_cells:
        i, j = random.choice(empty_cells)
        mat[i][j] = 2


def get_current_state(mat):
    for row in mat:
        if 2048 in row:
            return "WON"

    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 0:
                return "GAME NOT OVER"

            if j < SIZE - 1 and mat[i][j] == mat[i][j + 1]:
                return "GAME NOT OVER"

            if i < SIZE - 1 and mat[i][j] == mat[i + 1][j]:
                return "GAME NOT OVER"

    return "LOST"


def compress(mat):
    changed = False
    new_mat = []

    for row in mat:
        values = [value for value in row if value != 0]
        new_row = values + [0] * (SIZE - len(values))

        if new_row != row:
            changed = True

        new_mat.append(new_row)

    return new_mat, changed


def merge(mat):
    changed = False

    for row in mat:
        for j in range(SIZE - 1):
            if row[j] != 0 and row[j] == row[j + 1]:
                row[j] *= 2
                row[j + 1] = 0
                changed = True

    return mat, changed


def reverse(mat):
    return [row[::-1] for row in mat]


def transpose(mat):
    return [list(row) for row in zip(*mat)]


def move_left(grid):
    new_grid, changed1 = compress(grid)
    new_grid, changed2 = merge(new_grid)
    new_grid, changed3 = compress(new_grid)

    return new_grid, changed1 or changed2 or changed3


def move_right(grid):
    new_grid, changed = move_left(reverse(grid))
    return reverse(new_grid), changed


def move_up(grid):
    new_grid, changed = move_left(transpose(grid))
    return transpose(new_grid), changed


def move_down(grid):
    new_grid, changed = move_right(transpose(grid))
    return transpose(new_grid), changed

def print_grid(mat):
    for row in mat:
        print("".join(f"{value:4}" for value in row))
        print()

def main():
    mat = start_game()
    print_grid(mat)

    while True:
        try:
            command = input("Press the command:").strip().lower()
        except EOFError:
            print("\nExiting the game.")
            break

        moves ={
            'w': move_up,
            's': move_down,
            'a': move_left,
            'd': move_right,   
        }

        if command not in moves:
            print("Invalid key Pressed!")
            continue

        mat, changed = moves[command](mat)

        if changed:
            add_new_2(mat)

        print_grid(mat)

        print(get_current_state(mat))
        status = get_current_state(mat)

        if status != "GAME NOT OVER":
            break   

if __name__ == "__main__":
    main()  





