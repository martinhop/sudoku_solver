






# prints output to scree
def print_grid(grid):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' | ')
        print("", end='\n')


# checks if current location is empty and assign location if true
def empty_location(grid):

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return None

# checks if num is valid
def valid(grid, num, pos):

    # checks valid in row
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False
    # checks if num is in column
    for i in range(len(grid)):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False
    # checks if num is in small 3x3 grid
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if grid[i][j] == num and (i,j) != pos:
                return False
    return True


def solve(grid):

    find = empty_location(grid)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(grid, i, (row, col)):
            grid[row][col] = i

            if solve(grid):
                return True

            grid[row][col] = 0

    return False
