import pygame
import sys
import heapq

WIDTH = 800
ROWS = 40
CELL = WIDTH // ROWS

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Visualizer")

class Node:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.x=row*CELL
        self.y=col*CELL
        self.color=WHITE
        self.neighbors=[]

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,CELL,CELL))

    def is_barrier(self):
        return self.color==BLACK

    def make_start(self):
        self.color=GREEN

    def make_end(self):
        self.color=RED

    def make_barrier(self):
        self.color=BLACK

    def make_visited(self):
        self.color=BLUE

    def make_path(self):
        self.color=YELLOW

    def reset(self):
        self.color=WHITE

    def update_neighbors(self,grid):
        self.neighbors=[]
        if self.row<ROWS-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row>0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col<ROWS-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col>0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])


def make_grid():
    grid=[]
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node=Node(i,j)
            grid[i].append(node)
    return grid


def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen,GREY,(0,i*CELL),(WIDTH,i*CELL))
        pygame.draw.line(screen,GREY,(i*CELL,0),(i*CELL,WIDTH))


def draw(screen,grid):
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(screen)
    draw_grid()
    pygame.display.update()


def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()


def dijkstra(draw,grid,start,end):
    count=0
    pq=[]
    heapq.heappush(pq,(0,count,start))

    dist={node:float("inf") for row in grid for node in row}
    dist[start]=0

    came_from={}

    while pq:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        current=heapq.heappop(pq)[2]

        if current==end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp=dist[current]+1

            if temp<dist[neighbor]:
                came_from[neighbor]=current
                dist[neighbor]=temp
                count+=1
                heapq.heappush(pq,(dist[neighbor],count,neighbor))
                neighbor.make_visited()

        draw()

        if current!=start:
            current.make_visited()

    return False


def get_clicked_pos(pos):
    x,y=pos
    row=x//CELL
    col=y//CELL
    return row,col


def main():
    grid=make_grid()

    start=None
    end=None

    running=True

    while running:
        draw(screen,grid)

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running=False

            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos)
                node=grid[row][col]

                if not start and node!=end:
                    start=node
                    start.make_start()

                elif not end and node!=start:
                    end=node
                    end.make_end()

                elif node!=end and node!=start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos)
                node=grid[row][col]
                node.reset()
                if node==start:
                    start=None
                elif node==end:
                    end=None

            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    dijkstra(lambda: draw(screen,grid),grid,start,end)

                if event.key==pygame.K_c:
                    start=None
                    end=None
                    grid=make_grid()

    pygame.quit()


main()
