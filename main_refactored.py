import math
import random

import pygame

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Square properties
NUM_SQUARES = 100
MIN_SIZE = 10
MAX_SIZE = 40

# Movement parameters
GLOBAL_MAX_SPEED = 6
ANGLE_JITTER = 0.15

# Display settings
BACKGROUND_COLOR = (255, 255, 255)
FPS = 60

# Behavior parameters
FLEE_DISTANCE = 100
FLEE_FORCE = 0.2

CHASE_DISTANCE = 100
CHASE_FORCE = 0.08

# Lifespan parameters
MIN_LIFE = 3
MAX_LIFE = 9


class Square:
    """Represents a moving square with behaviors like fleeing, chasing, and boundary bouncing."""  # Docstring added to explain class purpose.
    def __init__(self) -> None:
        """Initialize a square with random size, position, velocity, color, and lifespan."""  # Docstring added to explain method purpose.
        self.size = random.randint(MIN_SIZE, MAX_SIZE)
        self.x = random.uniform(0, WIDTH - self.size)
        self.y = random.uniform(0, HEIGHT - self.size)

        self.max_speed = GLOBAL_MAX_SPEED * (MIN_SIZE / self.size)

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, self.max_speed)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        self.life_span = random.uniform(MIN_LIFE, MAX_LIFE)
        self.age = 0.0

    def center_x(self) -> float:
        """Calculate the x-coordinate of the square's center."""  # Docstring added to explain method purpose.
        return self.x + self.size / 2

    def center_y(self) -> float:
        """Calculate the y-coordinate of the square's center."""  # Docstring added to explain method purpose.
        return self.y + self.size / 2

    def apply_jitter(self) -> None:  # Added type hints for clarity and error prevention.
        """Apply random angular jitter to the square's velocity."""  # Docstring added to explain method purpose.
        speed = math.hypot(self.dx, self.dy)
        angle = math.atan2(self.dy, self.dx)
        angle += random.uniform(-ANGLE_JITTER, ANGLE_JITTER)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def limit_speed(self) -> None:  # Added type hints for clarity and error prevention.
        """Limit the square's speed to its maximum allowed value."""  # Docstring added to explain method purpose.
        speed = math.hypot(self.dx, self.dy)
        if speed > self.max_speed and speed != 0:
            scale = self.max_speed / speed
            self.dx *= scale
            self.dy *= scale

    # Extracted boundary checking to improve modularity.
    def _check_boundaries(self) -> None:
        """Check and handle collisions with window boundaries."""  # Docstring added to explain method purpose.
        if self.x <= 0:
            self.x = 0
            self.dx *= -1
        elif self.x + self.size >= WIDTH:
            self.x = WIDTH - self.size
            self.dx *= -1

        if self.y <= 0:
            self.y = 0
            self.dy *= -1
        elif self.y + self.size >= HEIGHT:
            self.y = HEIGHT - self.size
            self.dy *= -1

    def flee(self, squares: list["Square"]) -> None:  # Added type hints for clarity and error prevention.
        """Make the square flee from larger nearby squares."""  # Docstring added to explain method purpose.
        for other in squares:
            if other is self:
                continue
            if self.size >= other.size:
                continue

            diff_x = self.center_x() - other.center_x()
            diff_y = self.center_y() - other.center_y()
            distance = math.hypot(diff_x, diff_y)

            if 0 < distance < FLEE_DISTANCE:
                self.dx += (diff_x / distance) * FLEE_FORCE
                self.dy += (diff_y / distance) * FLEE_FORCE

    def chase(self, squares: list["Square"]) -> None:  # Added type hints for clarity and error prevention.
        """Make the square chase smaller nearby squares."""  # Docstring added to explain method purpose.
        # Renamed variables for better readability.
        for other in squares:
            if other is self:
                continue
            if self.size <= other.size:
                continue

            distance_x = other.center_x() - self.center_x()
            distance_y = other.center_y() - self.center_y()
            distance = math.hypot(distance_x, distance_y)

            if distance < CHASE_DISTANCE:
                if distance_x > 0:
                    self.dx += CHASE_FORCE
                else:
                    self.dx -= CHASE_FORCE

                if distance_y > 0:
                    self.dy += CHASE_FORCE
                else:
                    self.dy -= CHASE_FORCE

    def move(self, squares: list["Square"], dt: float) -> None:  # Added type hints for clarity and error prevention.
        """Update the square's position and apply behaviors."""  # Docstring added to explain method purpose.
        self.apply_jitter()
        self.flee(squares)
        self.chase(squares)
        self.limit_speed()

        self.x += self.dx * dt * FPS
        self.y += self.dy * dt * FPS

        # Call boundary check here.
        self._check_boundaries()

    def draw(self, screen: pygame.Surface) -> None:  # Added type hints for clarity and error prevention.
        """Draw the square on the screen."""  # Docstring added to explain method purpose.
        pygame.draw.rect(
            screen,
            self.color,
            (int(self.x), int(self.y), self.size, self.size),
        )


def main() -> None:  # Added type hints for clarity and error prevention.
    """Run the main game loop for the moving squares simulation."""  # Docstring added to explain method purpose.
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    squares: list[Square] = [Square() for _ in range(NUM_SQUARES)]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for i in range(len(squares)):
            squares[i].age += dt

            if squares[i].age >= squares[i].life_span:
                squares[i] = Square()

            squares[i].move(squares, dt)
            squares[i].draw(screen)

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()