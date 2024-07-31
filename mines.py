import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
CELL_SIZE = 80
NUM_MINES = 4
MARGIN = 20
TOP_MARGIN = 60
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

# Colors
BG_COLOR = (192, 192, 192)
CELL_COLOR = (128, 128, 128)
MINE_COLOR = (255, 0, 0)
FLAG_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)
REVEALED_COLOR = (211, 211, 211)
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Create grid
def create_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < NUM_MINES:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[y][x] = -1
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == -1:
                continue
            count = sum((nx, ny) in mines for nx in range(x-1, x+2) for ny in range(y-1, y+2) if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE)
            grid[y][x] = count
    return grid, mines

# Draw grid
def draw_grid(grid, revealed, flagged):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE + MARGIN, y*CELL_SIZE + TOP_MARGIN, CELL_SIZE, CELL_SIZE)
            if revealed[y][x]:
                pygame.draw.rect(screen, REVEALED_COLOR, rect)
                if grid[y][x] == -1:
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, CELL_SIZE//4)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, TEXT_COLOR)
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, CELL_COLOR, rect)
                if flagged[y][x]:
                    pygame.draw.rect(screen, FLAG_COLOR, rect)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 1)

# Draw reset button
def draw_reset_button():
    button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    text = small_font.render("Reset", True, BUTTON_TEXT_COLOR)
    screen.blit(text, text.get_rect(center=button_rect.center))
    return button_rect

# Main game loop
def main():
    grid, mines = create_grid()
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    start_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = (event.pos[0] - MARGIN) // CELL_SIZE, (event.pos[1] - TOP_MARGIN) // CELL_SIZE
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    if not game_over:
                        if event.button == 1 and not flagged[y][x]:  # Left click
                            revealed[y][x] = True
                            if grid[y][x] == -1:
                                game_over = True
                        elif event.button == 3:  # Right click
                            flagged[y][x] = not flagged[y][x]
                if game_over:
                    button_rect = draw_reset_button()
                    if button_rect.collidepoint(event.pos):
                        main()

        screen.fill(BG_COLOR)
        draw_grid(grid, revealed, flagged)

        # Draw timer
        elapsed_time = int(time.time() - start_time)
        timer_text = small_font.render(f"Time: {elapsed_time}s", True, TEXT_COLOR)
        screen.blit(timer_text, (MARGIN, MARGIN))

        # Check win condition
        if all(revealed[y][x] or (grid[y][x] == -1 and flagged[y][x]) for y in range(GRID_SIZE) for x in range(GRID_SIZE)):
            game_over = True
            win_text = font.render("You Win!", True, TEXT_COLOR)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, MARGIN))

        # Check game over
        if game_over:
            game_over_text = font.render("Game Over", True, TEXT_COLOR)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

            # Draw reset button
            draw_reset_button()

        pygame.display.flip()

if __name__ == "__main__":
    main()
