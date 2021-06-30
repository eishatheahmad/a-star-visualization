import pygame
import math
from queue import PriorityQueue

import random
import time
import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_dynamic_barrier(self):
        self.color=BLUE

    def reset_dynamic_barrier(self):
        self.color=YELLOW

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

#check up down left right to see if barriers
    def update_neighbors(self,grid):
        self.neighbors=[]

        #if down
        if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        #if up
        if self.row >0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        #if right
        if self.col < self.total_rows -1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        #if left
        if self.col >0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current= came_from[current]
        current.make_path()
        time.sleep(0.25)
        draw()


def algorithm(draw, grid, start, end,rows,width):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    keep_start=start

    new_obstacle = {}
    obstacle_count = 0
    dynamic = 5
    option = 0
    factor=6

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw) #
            end.make_end()
            keep_start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            dynamic=dynamic+0.1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    option+=1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

                    #def make_dynamic_barriers(rows, grid, start, end, count, new_obstacle):

                    print(count)
                    if option >=factor:
                        option = 0
                        factor = factor*2
                        row1 = int(random.randint(0, rows) % rows)
                        col1 = int(random.randint(0, rows) % rows)
                        new_goal = grid[row1][col1]
                        if new_goal is not start and new_goal is not RED and not new_goal.is_barrier():
                            new_goal.make_end()
                            end.reset()
                            end = new_goal
                            winsound.Beep(frequency, duration)




                    k= random.randint(0,1)
                    if k==0 and dynamic>1:
                        make_dynamic_barriers(rows,grid,start,end,obstacle_count,new_obstacle)
                        dynamic=dynamic-3

                    time.sleep(0.25)
        #def get_random_barriers(value,rows,grid,start,end):





        draw()

        if current != start:
            current.make_closed()
            time.sleep(0.25)

    return False




def make_dynamic_barriers(rows,grid,start,end,obstacle_count,new_obstacle):

    while obstacle_count < 10:
        x = int(random.randint(0, rows) % rows)
        y = int(random.randint(0, rows) % rows)
        new_barrier = grid[x][y]
        i = random.randint(1, 10)

        if i % 2 != 0:
            if new_barrier is not start and new_barrier is not end and new_barrier.is_barrier()==False and new_barrier.color is not RED:
                #print("adding barrier")
                new_barrier.make_dynamic_barrier()
                new_obstacle[obstacle_count] = new_barrier
                obstacle_count = obstacle_count + 1

        if i % 2 == 0:
            if obstacle_count > 0:
               # print("removing barrier")
                remove_barrier = new_obstacle[obstacle_count - 1]
                remove_barrier.reset()
                obstacle_count = obstacle_count - 1
                new_obstacle[obstacle_count] = None




def make_grid(rows, width):
    grid = []
    gap = (width // rows)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def get_random_barriers(value,rows,grid,start,end):


    for i in range(rows):
        spot=grid[0][i]
        spot.make_barrier()

    for i in range(rows):
        spot = grid[rows-1][i]
        spot.make_barrier()

    for i in range(rows):
        spot = grid[i][0]
        spot.make_barrier()
    for i in range(rows):
        spot = grid[i][rows-1]
        spot.make_barrier()



    count= ((value)//100) * (rows*rows)

    x= random.randint(0,rows)
    y= random.randint(0,rows)

    spot=grid[x%rows][y%rows]

    if spot!= start and spot != end and spot.is_barrier()==False:
        spot.make_barrier();

    return x,y






def main(win, width):

    num= int(input("Press 1 for 20*20 grid \nPress 2 for 40*40 grid \nPress 3 for 60*60 grid\n"))
    ROWS=0

    while(True):

        ROWS = 0
        if num==1:
            ROWS=20
            break
        elif num==2:
            ROWS=40
            break
        elif num==3:
            ROWS=40
            break
        num = int(input("Press 1 for 20*20 grid \nPress 2 for 40*40 grid \nPress 3 for 60*60 grid\n"))



    print(ROWS)


    obstacles=int(input("Enter percentage number of obstacles you want (e.g. 20, 50 etc)\n"))
    value=obstacles
    start = None
    end = None

    run = True

    percent= (value / 100.0)*(ROWS*ROWS)
    #since we have to make dynamic obstacles as well, we keep initial value less of obstacles
    percent = abs(percent-10)
    print(percent)
    grid = make_grid(ROWS, width)



    for i in range(int(percent)):
        get_random_barriers(value, ROWS, grid, start, end)


    while run:
            draw(win, grid, ROWS, width)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False



                if pygame.mouse.get_pressed()[0]: # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot!=end and spot != start:
                        spot.make_barrier()


                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()

                    if(spot==start):
                        start=None
                    elif spot==end:
                        end=None

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end,ROWS,width)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(ROWS,width)




    pygame.quit()

main(WIN, WIDTH)

