import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Constants
BOARD_SIZE = 10
TILE_SIZE = 80  # Larger tiles for better visibility
SIDEBAR_WIDTH = 400  # Wider sidebar
SCREEN_WIDTH = TILE_SIZE * BOARD_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = TILE_SIZE * BOARD_SIZE



# Initialize Pygame Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakes and Ladders")



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Load assets (e.g., player tokens, dice images) later
player_positions = [0, 0]  # Player positions on the board

# Snakes and Ladders Dictionary
snakes_and_ladders = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78,
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100,
}



def draw_snakes_and_ladders():
    for start, end in snakes_and_ladders.items():
        start_x, start_y = get_tile_center(start)
        end_x, end_y = get_tile_center(end)

        color = RED if start > end else GREEN  # Red for snakes, green for ladders
        pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 5)

def get_tile_center(tile):
    row = (tile - 1) // BOARD_SIZE
    col = (tile - 1) % BOARD_SIZE

    # Reverse the column for even rows (zigzag pattern)
    if row % 2 == 1:
        col = BOARD_SIZE - 1 - col

    x = col * TILE_SIZE + TILE_SIZE // 2
    y = SCREEN_HEIGHT - (row * TILE_SIZE + TILE_SIZE // 2)
    return x, y



def draw_sidebar(current_roll):
    # Sidebar background
    sidebar_rect = pygame.Rect(SCREEN_HEIGHT, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, (230, 230, 230), sidebar_rect)

    # Draw Dice
    dice_image = dice_images[current_roll - 1]
    dice_x = SCREEN_HEIGHT + (SIDEBAR_WIDTH - TILE_SIZE) // 2
    dice_y = SCREEN_HEIGHT // 4
    screen.blit(dice_image, (dice_x, dice_y))

    # Display current player info
    font = pygame.font.SysFont(None, 36)
    player_text = font.render(f"Player {current_player + 1}'s Turn", True, BLACK)
    screen.blit(player_text, (dice_x - 40, dice_y + TILE_SIZE + 20))




# Draw Board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            tile_number = row * BOARD_SIZE + col + 1

            # Adjust for zigzag numbering
            if row % 2 == 1:
                tile_number = row * BOARD_SIZE + (BOARD_SIZE - col)

            x = col * TILE_SIZE
            y = SCREEN_HEIGHT - (row + 1) * TILE_SIZE

            pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 1)

            # Display the tile number
            font = pygame.font.SysFont(None, 24)
            text = font.render(str(tile_number), True, BLACK)
            screen.blit(text, (x + TILE_SIZE // 4, y + TILE_SIZE // 4))


# Load dice images (assume you have six images named dice1.png, dice2.png, ..., dice6.png)
dice_images = [pygame.image.load(f"dice{i}.png") for i in range(1, 7)]



# Roll Dice
import time

def roll_dice():
    for _ in range(10):  # Animation loop
        dice_face = random.randint(1, 6)
        draw_sidebar(dice_face)  # Update sidebar with dice animation
        pygame.display.flip()
        pygame.time.delay(1)  # Short delay for smooth animation
    return dice_face


# Move Player
def move_player(player_index, steps):
    player_positions[player_index] += steps
    if player_positions[player_index] in snakes_and_ladders:
        player_positions[player_index] = snakes_and_ladders[player_positions[player_index]]

def ai_turn():
    steps = roll_dice()
    move_player(1, steps)  # Assuming AI is Player 2 (index 1)
    if player_positions[1] >= 100:
        print("AI wins!")
        return True
    return False


def animate_movement(player_index, start, end):
    steps = 50  # Smoother animation with more steps
    start_x, start_y = get_tile_center(start)
    end_x, end_y = get_tile_center(end)
    
    # Start the time at which animation begins
    start_time = pygame.time.get_ticks()

    # Track how much time has passed for smooth animation
    while True:
        # Calculate elapsed time
        elapsed_time = pygame.time.get_ticks() - start_time
        progress = min(elapsed_time / 500, 1)  # Faster progress (500ms per tile)

        # Calculate the intermediate position based on progress
        x = start_x + (end_x - start_x) * progress
        y = start_y + (end_y - start_y) * progress

        # Redraw the board and static tokens before the moving token
        draw_board()
        draw_snakes_and_ladders()
        draw_sidebar(current_roll)

        # Draw all static player positions
        for j, pos in enumerate(player_positions):
            if j != player_index and pos > 0:
                px, py = get_tile_center(pos)
                color = (255, 0, 0) if j == 0 else (0, 255, 0)
                pygame.draw.circle(screen, color, (px, py), TILE_SIZE // 4)

        # Draw the moving token
        pygame.draw.circle(screen, (255, 0, 0) if player_index == 0 else (0, 255, 0), (x, y), TILE_SIZE // 4)

        pygame.display.flip()

        # Stop animation when it reaches the target
        if progress >= 1:
            break

        # Limit frame rate to avoid hogging CPU resources
        pygame.time.Clock().tick(60)  # Cap frame rate to 60 FPS




def move_player(player_index, steps):
    start = player_positions[player_index]
    for _ in range(steps):
        start += 1
        animate_movement(player_index, player_positions[player_index], start)
        player_positions[player_index] = start

    # Check for snakes or ladders and animate further if needed
    if player_positions[player_index] in snakes_and_ladders:
        end = snakes_and_ladders[player_positions[player_index]]
        animate_movement(player_index, player_positions[player_index], end)
        player_positions[player_index] = end




# Game Loop
# Game Loop
running = True
current_player = 0
ai_enabled = True
current_roll= 1


while running:
    draw_board()
    draw_snakes_and_ladders()
    draw_sidebar(current_roll)

    # Draw player tokens
    for i, pos in enumerate(player_positions):
        if pos > 0:
            x, y = get_tile_center(pos)
            pygame.draw.circle(screen, RED if i == 0 else GREEN, (x, y), TILE_SIZE // 4)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and current_player == 0:
            if event.key == pygame.K_SPACE:
                current_roll = roll_dice()
                move_player(current_player, current_roll)
                if player_positions[current_player] >= 100:
                    print(f"Player {current_player + 1} wins!")
                    running = False
                current_player = (current_player + 1) % len(player_positions)

    if ai_enabled and current_player == 1:
        current_roll = roll_dice()
        move_player(current_player, current_roll)
        if player_positions[current_player] >= 100:
            print("AI wins!")
            running = False
        current_player = (current_player + 1) % len(player_positions)




pygame.quit()
