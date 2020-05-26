import pygame
import time

pygame.font.init()

#RGB colors for screen GUI
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)

#Set-up initial screen
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku Solver')



class Grid():
    board = [
        [9, 1, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 5, 0, 4, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 9, 0, 3, 0, 5, 0, 6],
        [0, 0, 0, 5, 9, 0, 4, 3, 0],
        [5, 0, 8, 0, 6, 0, 0, 1, 2],
        [0, 0, 5, 0, 7, 0, 0, 0, 9],
        [0, 0, 6, 0, 0, 0, 1, 5, 8],
        [0, 0, 0, 2, 5, 6, 0, 0, 0]]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cells =[[Cell(self.board[i][j], i, j, width, height) for j in range(cols) for i in range(rows)]]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        pass

    def place(self):
        pass

    def sketch(self, val):
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self, win):

        # draw grid to screen
        space = self.width / 9
        for i in range(self.rows+1):
            if i %3 == 0 and i != 0:
                line_weight = 4
            else:
                line_weight = 1

            pygame.draw.line(WIN, black, (130, i* gap), (self.width, i*gap), line_weight)
            pygame.draw.line(WIN, black, (i*gap, 100), (i*gap, self.height), line_weight)

        #draw cells to screen
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(WIN)

    def select(self, row, col):
        #deselects all other cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        #selects required cell
        self.cells[row][col].selected = True
        self.selected = (row, col)


    def clear(self):

        row, col = self.selected

        if self.cells[row][col] == 0:
            self.cells[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row,col)
        """

        if pos[0] < self.width and pos[1] < self.height:
            space = self.width/9
            x = pos[0] // space
            y = pos[1] // space
            return (int(x), int(y))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j] == 0:
                    return False
        return True

class Cell():
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

    def draw(self, win):
        numfont = pygame.font.SysFont('calibri', 40)

        space = self.width / 9
        x = self.col * space
        y = self.row * space

        if self.temp != 0 and self.value == 0:
            num = numfont.render(str(self.temp), 1, grey)
            WIN.blit(num, (x+5, y+5))
        elif not self.value == 0:
            num = numfont.render(str(self.value), 1, black)
            WIN.blit(num, (x + (space/2 - num.get_width()/2), y + (space/2 - num.get_height()/2)))

        if self.selected:
            pygame.draw.rect(WIN, green, (x, y, space, space), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time, strikes):
    win.fill(white)
    titlefont = pygame.font.SysFont('calibri', 50)
    font = pygame.font.SysFont('calibri', 40)
    #Displays the title
    titlelabel = titlefont.render('Sudoku Solver', 1, red)
    win.blit(titlelabel, (WIDTH / 2 - titlelabel.get_width() / 2, 10))
    #Display time
    text = font.render("Time: " + format_time(time), 1, black)
    win.blit(text, (800-160, 700))
    #incorrect guesses
    text = font.render("X" * strikes, 1, red)
    win.blit(text, (160, 700))
    #Draw board and grid
    board.draw(win)

def format_time(secs):
    sec = secs%60
    min = secs//60
    #hour = min//60

    for_time = str(min) + ':' + str(sec)
    return for_time

def main():
    key = None
    run = True
    board = Grid(9, 9, 540, 540)
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cells[i][j].temp != 0:
                        if board.place(board.cells[i][j].temp):
                            print('Success')
                        else:
                            print(Wrong)
                            strikes += 1
                            key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(WIN, board, play_time, strikes)
        pygame.display.update()

main()

