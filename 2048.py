import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SIZE = 400
GRID_SIZE = 4
CELL_SIZE = SIZE // GRID_SIZE
FONT = pygame.font.SysFont("arial", 40, bold=True)

# Couleurs
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Création de la fenêtre
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("2048")

# Initialisation de la grille
def init_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

# Ajouter une nouvelle tuile (2 ou 4)
def add_new_tile(grid):
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4

# Déplacement et fusion
def compress_and_merge(row):
    row = [num for num in row if num != 0]
    for i in range(len(row) - 1):
        if row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    row = [num for num in row if num != 0]
    while len(row) < GRID_SIZE:
        row.append(0)
    return row

def move_left(grid):
    return [compress_and_merge(row) for row in grid]

def move_right(grid):
    return [compress_and_merge(row[::-1])[::-1] for row in grid]

def move_up(grid):
    return list(map(list, zip(*move_left(list(zip(*grid))))))

def move_down(grid):
    return list(map(list, zip(*move_right(list(zip(*grid))))))

# Vérification de la victoire et des mouvements possibles
def is_winner(grid):
    return any(2048 in row for row in grid)

def can_move(grid):
    for row in grid:
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1] or row[i] == 0 or row[i + 1] == 0:
                return True
    for col in zip(*grid):
        for i in range(GRID_SIZE - 1):
            if col[i] == col[i + 1] or col[i] == 0 or col[i + 1] == 0:
                return True
    return False

# Affichage de la grille
def draw_grid(grid):
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = CELL_COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=10)

            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0) if value < 8 else (255, 255, 255))
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

# Calcul du score
def calculate_score(grid):
    return sum(sum(row) for row in grid)

# Boucle principale
def main():
    grid = init_grid()
    running = True

    while running:
        draw_grid(grid)
        score = calculate_score(grid)
        pygame.display.set_caption(f"2048 | Score : {score}")

        if is_winner(grid):
            print("🎉 Bravo ! Tu as atteint 2048 !")
            running = False

        if not can_move(grid):
            print("💀 Game Over ! Plus de mouvements possibles.")
            running = False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_grid = move_left(grid)
                elif event.key == pygame.K_RIGHT:
                    new_grid = move_right(grid)
                elif event.key == pygame.K_UP:
                    new_grid = move_up(grid)
                elif event.key == pygame.K_DOWN:
                    new_grid = move_down(grid)
                else:
                    continue

                if new_grid != grid:
                    grid = new_grid
                    add_new_tile(grid)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
