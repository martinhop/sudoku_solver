testgrid = [
     [9, 1, 0, 4, 0, 0, 0, 0, 0],
     [0, 0, 7, 0, 0, 5, 0, 4, 0],
     [0, 0, 4, 0, 0, 0, 0, 0, 0],
     [0, 0, 9, 0, 3, 0, 5, 0, 6],
     [0, 0, 0, 5, 9, 0, 4, 3, 0],
     [5, 0, 8, 0, 6, 0, 0, 1, 2],
     [0, 0, 5, 0, 7, 0, 0, 0, 9],
     [0, 0, 6, 0, 0, 0, 1, 5, 8],
     [0, 0, 0, 2, 5, 6, 0, 0, 0]]

 #prints output to scree
def print_grid(grid):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=' | ')
        print("", end='\n')


 #checks if current location is empty and assign location if true
def empty_location(grid, location):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                location[0] = i
                location[1] = j
                return True
    return False

 # checks if num is in row
def used_in_row(grid, row, num):
    for j in range(9):
        if grid[row][j] == num:
            return True
    return False


 # checks if num is in column
def used_in_col(grid, col, num):
    for i in range(9):
        if grid[i][col] == num:
            return True
    return False


 # checks if num is in small 3x3 grid
def used_in_box(grid, row, col, num):
    for i in range(3):
        for j in range(3):
            if grid[i + row][j + col] == num:
                return True
    return False


def move_ok(grid, row, col, num):
    return valid1(grid, num, (row,col))
    return not used_in_row(grid, row, num) and not used_in_col(grid, col, num) and not used_in_box(grid, row - row % 3, col - col % 3, num)

def valid1(grid, num, pos):

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

def solver(grid):

    location = [0, 0]

    if not empty_location(testgrid, location):
        return True

    row = location[0]
    col = location[1]

    for num in range(1, 10):

        if (move_ok(testgrid, row, col, num)):

            testgrid[row][col] = num
            if solver(testgrid):
                return True

            testgrid[row][col] = 0

    return False



if __name__=="__main__":

    if solver(testgrid):
        print_grid(testgrid)
    else:
        print('No possible solution!')