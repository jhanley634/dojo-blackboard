# code from Sam Miraz in the dojo #python channel

import math
import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
MAZE_WIDTH = 28
MAZE_HEIGHT = 31
WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE
WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 50  # Extra space for score and lives

# Colors
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 100)
WALL_BLUE = (33, 33, 222)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
WHITE = (255, 255, 255)
FRIGHTENED_BLUE = (50, 50, 255)

# Maze layout (1 = wall, 0 = path, 2 = dot, 3 = power pellet)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Create a copy for resetting
ORIGINAL_MAZE = [row[:] for row in MAZE]


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.direction = None
        self.next_direction = None
        self.speed = 2
        self.mouth_angle = 0
        self.mouth_opening = True

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = None
        self.next_direction = None

    def update(self):
        # Animate mouth
        if self.mouth_opening:
            self.mouth_angle += 2
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= 2
            if self.mouth_angle <= 0:
                self.mouth_opening = True

        # Try to change direction if requested
        if self.next_direction:
            new_x, new_y = self.get_next_position(self.next_direction)
            if self.can_move(new_x, new_y):
                self.direction = self.next_direction
                self.next_direction = None

        # Move in current direction
        if self.direction:
            new_x, new_y = self.get_next_position(self.direction)
            if self.can_move(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def get_next_position(self, direction):
        new_x, new_y = self.x, self.y
        if direction == "UP":
            new_y -= self.speed
        elif direction == "DOWN":
            new_y += self.speed
        elif direction == "LEFT":
            new_x -= self.speed
        elif direction == "RIGHT":
            new_x += self.speed
        return new_x, new_y

    def can_move(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)

        if grid_x < 0 or grid_x >= MAZE_WIDTH or grid_y < 0 or grid_y >= MAZE_HEIGHT:
            return False

        checks = [
            (grid_x, grid_y),
            (int((x + CELL_SIZE // 2) // CELL_SIZE), grid_y),
            (grid_x, int((y + CELL_SIZE // 2) // CELL_SIZE)),
        ]

        for gx, gy in checks:
            if gx < MAZE_WIDTH and gy < MAZE_HEIGHT:
                if MAZE[gy][gx] == 1:
                    return False
        return True

    def draw(self, screen):
        center_x = int(self.x + CELL_SIZE // 2)
        center_y = int(self.y + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2

        # Determine rotation based on direction
        rotation = 0
        if self.direction == "RIGHT":
            rotation = 0
        elif self.direction == "DOWN":
            rotation = 90
        elif self.direction == "LEFT":
            rotation = 180
        elif self.direction == "UP":
            rotation = 270

        # Draw Pacman with animated mouth
        if self.direction and self.mouth_angle > 5:
            # Draw partial circle (Pacman with open mouth)
            start_angle = math.radians(rotation + self.mouth_angle)
            end_angle = math.radians(rotation + 360 - self.mouth_angle)

            # Create points for the pie shape
            points = [(center_x, center_y)]
            for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1, 5):
                rad = math.radians(angle)
                px = center_x + radius * math.cos(rad)
                py = center_y + radius * math.sin(rad)
                points.append((px, py))
            points.append((center_x, center_y))

            pygame.draw.polygon(screen, YELLOW, points)
        else:
            # Draw full circle when mouth is closed or not moving
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)


class Ghost:
    def __init__(self, x, y, color=PINK):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.speed = 1.5
        self.color = color
        self.frightened = False
        self.frightened_timer = 0
        self.flash_timer = 0

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.frightened = False
        self.frightened_timer = 0

    def set_frightened(self):
        self.frightened = True
        self.frightened_timer = 300  # 5 seconds at 60 FPS

    def update(self, player):
        # Update frightened mode
        if self.frightened:
            self.frightened_timer -= 1
            self.flash_timer += 1
            if self.frightened_timer <= 0:
                self.frightened = False
                self.frightened_timer = 0

        # AI behavior
        if self.frightened:
            # Run away from player randomly
            if random.random() < 0.1:
                self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        else:
            # Chase player
            dx = player.x - self.x
            dy = player.y - self.y

            possible_dirs = []
            if abs(dx) > abs(dy):
                if dx > 0:
                    possible_dirs.append("RIGHT")
                else:
                    possible_dirs.append("LEFT")
            else:
                if dy > 0:
                    possible_dirs.append("DOWN")
                else:
                    possible_dirs.append("UP")

            # Add some randomness
            if random.random() < 0.3:
                possible_dirs = ["UP", "DOWN", "LEFT", "RIGHT"]

            # Try to move in preferred direction
            for dir in possible_dirs:
                new_x, new_y = self.get_next_position(dir)
                if self.can_move(new_x, new_y):
                    self.direction = dir
                    break

        # Move
        new_x, new_y = self.get_next_position(self.direction)
        if self.can_move(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def get_next_position(self, direction):
        new_x, new_y = self.x, self.y
        speed = self.speed * 0.5 if self.frightened else self.speed
        if direction == "UP":
            new_y -= speed
        elif direction == "DOWN":
            new_y += speed
        elif direction == "LEFT":
            new_x -= speed
        elif direction == "RIGHT":
            new_x += speed
        return new_x, new_y

    def can_move(self, x, y):
        grid_x = int(x // CELL_SIZE)
        grid_y = int(y // CELL_SIZE)

        if grid_x < 0 or grid_x >= MAZE_WIDTH or grid_y < 0 or grid_y >= MAZE_HEIGHT:
            return False

        checks = [
            (grid_x, grid_y),
            (int((x + CELL_SIZE // 2) // CELL_SIZE), grid_y),
            (grid_x, int((y + CELL_SIZE // 2) // CELL_SIZE)),
        ]

        for gx, gy in checks:
            if gx < MAZE_WIDTH and gy < MAZE_HEIGHT:
                if MAZE[gy][gx] == 1:
                    return False
        return True

    def draw(self, screen):
        center_x = int(self.x + CELL_SIZE // 2)
        center_y = int(self.y + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2

        # Choose color based on frightened state
        if self.frightened:
            if self.frightened_timer < 120 and self.flash_timer % 20 < 10:
                ghost_color = WHITE
            else:
                ghost_color = FRIGHTENED_BLUE
        else:
            ghost_color = self.color

        # Draw ghost body (rounded top)
        pygame.draw.circle(screen, ghost_color, (center_x, center_y - 2), radius)
        pygame.draw.rect(screen, ghost_color, (self.x + 2, center_y - 2, CELL_SIZE - 4, radius + 2))

        # Draw wavy bottom
        wave_width = (CELL_SIZE - 4) // 3
        for i in range(3):
            wave_x = self.x + 2 + i * wave_width
            wave_y = self.y + CELL_SIZE - 3
            points = [
                (wave_x, wave_y - 3),
                (wave_x + wave_width // 2, wave_y),
                (wave_x + wave_width, wave_y - 3),
                (wave_x + wave_width, center_y - 2),
                (wave_x, center_y - 2),
            ]
            pygame.draw.polygon(screen, ghost_color, points)

        # Draw eyes (not when frightened)
        if not self.frightened:
            eye_radius = 3
            left_eye_x = center_x - 4
            right_eye_x = center_x + 4
            eye_y = center_y - 3

            # White part of eyes
            pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_radius)

            # Pupils (look in direction of movement)
            pupil_offset = 1
            pupil_x_offset = 0
            pupil_y_offset = 0

            if self.direction == "LEFT":
                pupil_x_offset = -pupil_offset
            elif self.direction == "RIGHT":
                pupil_x_offset = pupil_offset
            elif self.direction == "UP":
                pupil_y_offset = -pupil_offset
            elif self.direction == "DOWN":
                pupil_y_offset = pupil_offset

            pygame.draw.circle(
                screen, DARK_BLUE, (left_eye_x + pupil_x_offset, eye_y + pupil_y_offset), 2
            )
            pygame.draw.circle(
                screen, DARK_BLUE, (right_eye_x + pupil_x_offset, eye_y + pupil_y_offset), 2
            )
        else:
            # Frightened eyes (simple white dots)
            pygame.draw.circle(screen, WHITE, (center_x - 4, center_y), 1)
            pygame.draw.circle(screen, WHITE, (center_x + 4, center_y), 1)
            pygame.draw.circle(screen, WHITE, (center_x - 2, center_y + 3), 1)
            pygame.draw.circle(screen, WHITE, (center_x + 2, center_y + 3), 1)


def draw_maze(screen):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if MAZE[y][x] == 1:
                # Draw wall with border for classic look
                pygame.draw.rect(
                    screen, WALL_BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
                pygame.draw.rect(
                    screen, DARK_BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1
                )
            elif MAZE[y][x] == 2:
                # Draw regular dot
                center_x = x * CELL_SIZE + CELL_SIZE // 2
                center_y = y * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 2)
            elif MAZE[y][x] == 3:
                # Draw power pellet (larger)
                center_x = x * CELL_SIZE + CELL_SIZE // 2
                center_y = y * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 5)


def check_dot_collision(player, ghost):
    grid_x = int(player.x // CELL_SIZE)
    grid_y = int(player.y // CELL_SIZE)

    if 0 <= grid_x < MAZE_WIDTH and 0 <= grid_y < MAZE_HEIGHT:
        if MAZE[grid_y][grid_x] == 2:
            MAZE[grid_y][grid_x] = 0
            return 10, False
        elif MAZE[grid_y][grid_x] == 3:
            MAZE[grid_y][grid_x] = 0
            ghost.set_frightened()
            return 50, True
    return 0, False


def check_ghost_collision(player, ghost):
    distance = ((player.x - ghost.x) ** 2 + (player.y - ghost.y) ** 2) ** 0.5
    return distance < CELL_SIZE


def count_remaining_dots():
    count = 0
    for row in MAZE:
        for cell in row:
            if cell == 2 or cell == 3:
                count += 1
    return count


def reset_maze():
    global MAZE
    MAZE = [row[:] for row in ORIGINAL_MAZE]


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pacman - Classic Edition - Sam Mirazi")
    clock = pygame.time.Clock()

    # Initialize player and ghost
    player = Player(CELL_SIZE * 1, CELL_SIZE * 23)
    ghost = Ghost(CELL_SIZE * 13, CELL_SIZE * 14, RED)

    # Game state
    score = 0
    lives = 3
    game_over = False
    game_won = False
    invincible_timer = 0

    font = pygame.font.Font(None, 28)
    big_font = pygame.font.Font(None, 48)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.next_direction = "UP"
                elif event.key == pygame.K_DOWN:
                    player.next_direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    player.next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    player.next_direction = "RIGHT"
                elif event.key == pygame.K_r and (game_over or game_won):
                    # Restart game
                    reset_maze()
                    player.reset()
                    ghost.reset()
                    score = 0
                    lives = 3
                    game_over = False
                    game_won = False
                    invincible_timer = 0

        if not game_over and not game_won:
            # Update game objects
            player.update()
            ghost.update(player)

            # Update invincibility timer
            if invincible_timer > 0:
                invincible_timer -= 1

            # Check dot collision
            points, power_pellet = check_dot_collision(player, ghost)
            if points > 0:
                score += points

            # Check if all dots collected
            if count_remaining_dots() == 0:
                game_won = True

            # Check ghost collision
            if check_ghost_collision(player, ghost) and invincible_timer == 0:
                if ghost.frightened:
                    # Eat ghost
                    score += 200
                    ghost.reset()
                    ghost.frightened = False
                else:
                    # Lose a life
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    else:
                        # Reset positions
                        player.reset()
                        ghost.reset()
                        invincible_timer = 120  # 2 seconds invincibility

        # Draw everything
        screen.fill(BLACK)
        draw_maze(screen)

        # Draw player (flash when invincible)
        if invincible_timer == 0 or invincible_timer % 10 < 5:
            player.draw(screen)

        ghost.draw(screen)

        # Draw HUD
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (10, WINDOW_HEIGHT - 40))

        # Draw lives
        lives_text = font.render(f"LIVES:", True, WHITE)
        screen.blit(lives_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 40))
        for i in range(lives):
            pygame.draw.circle(screen, YELLOW, (WINDOW_WIDTH - 80 + i * 25, WINDOW_HEIGHT - 28), 8)

        # Draw game over or win message
        if game_over:
            game_over_text = big_font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to Restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    text_rect.x - 10,
                    text_rect.y - 10,
                    text_rect.width + 20,
                    restart_rect.bottom - text_rect.top + 20,
                ),
            )
            screen.blit(game_over_text, text_rect)
            screen.blit(restart_text, restart_rect)

        if game_won:
            win_text = big_font.render("YOU WIN!", True, YELLOW)
            restart_text = font.render("Press R to Restart", True, WHITE)
            text_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    text_rect.x - 10,
                    text_rect.y - 10,
                    text_rect.width + 20,
                    restart_rect.bottom - text_rect.top + 20,
                ),
            )
            screen.blit(win_text, text_rect)
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
