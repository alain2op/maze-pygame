import pygame
import random

# Maze dimensions
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Maze Generation")

# Initialize grid
grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Recursive Backtracking algorithm
def recursive_backtracking_maze(x, y):
    grid[x][y] = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + 2*dx, y + 2*dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny]:
            grid[x+dx][y+dy] = 0
            recursive_backtracking_maze(nx, ny)

# Generate maze
recursive_backtracking_maze(1, 1)

# Draw maze
def draw_maze():
    screen.fill(WHITE)
    for x in range(ROWS):
        for y in range(COLS):
            if grid[x][y]:
                pygame.draw.rect(screen, BLACK, (y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_maze()

pygame.quit()
