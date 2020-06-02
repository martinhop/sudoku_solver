import pygame
import time
from sudoku_solver import valid, solve, autosolver
import sudoku_generator

pygame.font.init()

# RGB colors for screen GUI
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
lgrey = (237, 237, 237)

# Set-up initial screen
WIDTH, HEIGHT = 800, 800
SURWIDTH, SURHEIGHT = 541, 541
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SUR = pygame.Surface((SURWIDTH, SURHEIGHT))
pygame.display.set_caption('Sudoku Game & Solver')
SCROFFSETX = (WIDTH / 2) - (SURWIDTH / 2)
SCROFFSETY = 75


class Grid:
    empty = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    gameboard = [
        [9, 1, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 5, 0, 4, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 9, 0, 3, 0, 5, 0, 6],
        [0, 0, 0, 5, 9, 0, 4, 3, 0],
        [5, 0, 8, 0, 6, 0, 0, 1, 2],
        [0, 0, 5, 0, 7, 0, 0, 0, 9],
        [0, 0, 6, 0, 0, 0, 1, 5, 8],
        [0, 0, 0, 2, 5, 6, 0, 0, 0]]

    def __init__(self, rows, cols, width, height, board):
        self.board = board
        self.rows = rows
        self.cols = cols
        print(self.board)
        self.cells = [[Cell(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):

        # updates the grid
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):

        # sets selected cell with value
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set(val)
            self.update_model()

        # checks if value is correct (if correct place it, if not remove it)
        if valid(self.model, val, (row, col)) and solve(self.model):
            self.board[row][col] = val
            return True
        else:
            self.cells[row][col].set(0)
            self.cells[row][col].set_temp(0)
            self.update_model()
            return False

    def autoplace(self):

        # uses autosolver function to complete grid
        self.update_model()
        self.board = autosolver(self.model)
        for i in range(9):
            for j in range(9):
                self.selected = i, j
                val = self.board[i][j]
                self.place(val)

    def sketch(self, val):

        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self, surface):

        # draw grid to screen
        space = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0 and i != 9:
                line_weight = 4
            else:
                line_weight = 1

            pygame.draw.line(surface, black, (0, i * space), (self.width, i * space), line_weight)
            pygame.draw.line(surface, black, (i * space, 0), (i * space, self.height), line_weight)

        # draw cells to screen
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(surface)

    def select(self, row, col):

        # deselects all other cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        # selects required cell
        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):

        # clear any temp number in selected cell
        row, col = self.selected

        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row,col)
        """
        # outer if statement accounts for screen offset placement
        if pos[0] > SCROFFSETX and pos[1] > SCROFFSETY:
            if pos[0] <= self.width + SCROFFSETX and pos[1] <= self.height + SCROFFSETY:
                space = (self.width / 9)
                x = ((pos[0] - SCROFFSETX) // space)
                y = ((pos[1] - SCROFFSETY) // space)
                return (int(x), int(y))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True


class Cell:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, surface):

        # draws cells to grid
        numfont = pygame.font.SysFont('calibri', 40)

        space = self.width / 9
        x = (self.col * space)
        y = (self.row * space)

        if self.temp != 0 and self.value == 0:
            num = numfont.render(str(self.temp), 1, grey)
            surface.blit(num, (x + 5, y + 5))
        elif not self.value == 0:
            num = numfont.render(str(self.value), 1, black)
            surface.blit(num, (x + (space / 2 - num.get_width() / 2), y + (space / 2 - num.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(surface, green, (x, y, space, space), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, surface, board, time, strikes, solved, solvermode):
    """Redraws main game GUI window"""
    win.fill(white)
    titlefont = pygame.font.SysFont('calibri', 50)
    font = pygame.font.SysFont('calibri', 40)

    # Displays the title
    titlelabel = titlefont.render('Sudoku Game & Solver', 1, red)
    win.blit(titlelabel, (WIDTH / 2 - titlelabel.get_width() / 2, 10))

    # Display time
    if not solvermode:
        text = font.render("Time: " + format_time(time), 1, black)
        win.blit(text, (WIDTH - SCROFFSETX - text.get_width(), 700))

        # incorrect guesses in game mode or instructions in solver mode
        text = font.render("X" * strikes, 1, red)
        win.blit(text, (SCROFFSETX, 700))
    else:
        text = font.render("Enter known numbers and press 'space' to solve board", 1, red)
        win.blit(text, (WIDTH/2 - text.get_width()/2, 700))


    # completed board
    if solved:
        finished = font.render('Game Over, press any key to continue', 1, red)
        win.blit(finished, (SCROFFSETX, 650))

    # Draw board and grid onto surface
    surface.fill(lgrey)
    board.draw(surface)
    win.blit(surface, (SCROFFSETX, SCROFFSETY))


def format_time(secs):
    sec = secs % 60
    min = secs // 60
    hour = min // 60

    (f"{1:02d}")

    for_time = f' {min:02d}:{sec:02d}'
    return for_time


# main game window
def main(solvermode):


    if solvermode:

        # generates an empty grid
        board = [[0]*9 for _ in range(9)]
    else:
        new = sudoku_generator.SudokuGenerator()
        board = new.generate_puzzle()
        print(board)

    key = None
    run = True
    board = Grid(9, 9, 540, 540, board)
    start = time.time()
    strikes = 0
    solved = False

    while run:
        if not solved:
            play_time = round(time.time() - start)

        # keyboard inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if not solved:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        key = 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        key = 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        key = 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        key = 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        key = 5
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        key = 6
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        key = 7
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        key = 8
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        key = 9
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        board.clear()
                        key = None
                    if event.key == pygame.K_RETURN:
                        i, j = board.selected
                        if board.cells[i][j].temp != 0:
                            if not board.place(board.cells[i][j].temp):
                                strikes += 1
                                if strikes == 3:
                                    solved = True
                            key = None
                    if event.key == pygame.K_SPACE:
                        key = None
                        board.autoplace()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[1], clicked[0])
                        key = None
            else:
                if event.type == pygame.KEYDOWN:
                    menu()

        if board.selected and key != None:
            board.sketch(key)

        if board.is_finished():
            solved = True

        redraw_window(WIN, SUR, board, play_time, strikes, solved, solvermode)
        pygame.display.update()


# main menu screen
def menu():
    run = True
    solvermode = False

    while run:

        WIN.fill(white)
        menufont = pygame.font.SysFont('calibri', 80)
        submenufont = pygame.font.SysFont('calibri', 60)
        menulabel1 = menufont.render('Suduko Game', 1, red)
        menulabel2 = menufont.render('&', 1, red)
        menulabel3 = menufont.render('Solver', 1, red)
        menulabel4 = submenufont.render("Press 'Space' to start game mode", 1, red)
        menulabel5 = submenufont.render("Press 'S' key to enter solver mode", 1, red)
        menulabel6 = submenufont.render("Press 'I' key for instructions", 1, red)
        WIN.blit(menulabel1, (WIDTH / 2 - menulabel1.get_width() / 2, 150))
        WIN.blit(menulabel2, (WIDTH / 2 - menulabel2.get_width() / 2, 200))
        WIN.blit(menulabel3, (WIDTH / 2 - menulabel3.get_width() / 2, 250))
        WIN.blit(menulabel4, (WIDTH / 2 - menulabel4.get_width() / 2, 400))
        WIN.blit(menulabel5, (WIDTH / 2 - menulabel5.get_width() / 2, 450))
        WIN.blit(menulabel6, (WIDTH / 2 - menulabel6.get_width() / 2, 600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    solvermode = True
                    main(solvermode)
                if event.key == pygame.K_SPACE:
                    main(solvermode)
                if event.key == pygame.K_i:
                    instructions()

        pygame.display.update()


# instruction screen
def instructions():
    run = True

    while run:

        WIN.fill(white)

        # setup fonts
        titlefont = pygame.font.SysFont('calibri', 50)
        insttitlefont = pygame.font.SysFont('calibri', 40)
        instfont = pygame.font.SysFont('calibri', 30)

        # setup labels
        titlelabel = titlefont.render('Instructions', 1, red)
        insttitle1 = insttitlefont.render("Game Play Mode", 1, red)
        instlabel1 = instfont.render("- From main menu press 'Space' to enter solver mode", 1, red)
        instlabel2 = instfont.render("- Select empty cell with mouse", 1, red)
        instlabel3 = instfont.render("- Enter value and hit enter to commit (max 3 strikes)", 1, red)
        instlabel4 = instfont.render("- To solve a board at any time press 'space'", 1, red)
        insttitle2 = insttitlefont.render("Solver Mode", 1, red)
        instlabel5 = instfont.render("- From main menu press 'S' to enter solver mode", 1, red)
        instlabel6 = instfont.render("- Enter known numbers into cleared grid", 1, red)
        instlabel7 = instfont.render("- To solve a board at any time press 'space'", 1, red)
        instlabel8 = instfont.render("Press 'escape' to return to main menu", 1, red)

        # draw elements to screen
        WIN.blit(titlelabel, (WIDTH / 2 - titlelabel.get_width() / 2, 50))
        WIN.blit(insttitle1, (WIDTH / 2 - insttitle1.get_width() / 2, 150))
        WIN.blit(instlabel1, (WIDTH / 2 - instlabel1.get_width() / 2, 200))
        WIN.blit(instlabel2, (WIDTH / 2 - instlabel2.get_width() / 2, 250))
        WIN.blit(instlabel3, (WIDTH / 2 - instlabel3.get_width() / 2, 300))
        WIN.blit(instlabel4, (WIDTH / 2 - instlabel4.get_width() / 2, 350))
        WIN.blit(insttitle2, (WIDTH / 2 - insttitle2.get_width() / 2, 450))
        WIN.blit(instlabel5, (WIDTH / 2 - instlabel5.get_width() / 2, 500))
        WIN.blit(instlabel6, (WIDTH / 2 - instlabel6.get_width() / 2, 550))
        WIN.blit(instlabel7, (WIDTH / 2 - instlabel7.get_width() / 2, 600))
        WIN.blit(instlabel8, (WIDTH / 2 - instlabel8.get_width() / 2, 700))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()

        pygame.display.update()


if __name__ == '__main__':
    menu()
