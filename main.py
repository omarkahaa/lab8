import math
import random

import pygame

WIDTH = 800
HEIGHT = 600

BIG_SQUARES = 5
MEDIUM_SQUARES = 10
SMALL_SQUARES = 30

BIG_SIZE = 25
MEDIUM_SIZE = 10
SMALL_SIZE = 4

MIN_SIZE = SMALL_SIZE
GLOBAL_MAX_SPEED = 6
ANGLE_JITTER = 0.15
BACKGROUND_COLOR = (255, 255, 255)
FPS = 60

FLEE_DISTANCE = 100
FLEE_FORCE = 0.2

CHASE_DISTANCE = 100
CHASE_FORCE = 0.08

MIN_LIFE = 3
MAX_LIFE = 9

MIN_BRIGHTNESS = 0.25


class Square:
    def __init__(self, size: int) -> None:
        self.size = size
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
        return self.x + self.size / 2

    def center_y(self) -> float:
        return self.y + self.size / 2

    def check_collision(self, other: "Square") -> bool:
        my_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        other_rect = pygame.Rect(other.x, other.y, other.size, other.size)

        return my_rect.colliderect(other_rect)

    def eat(self, squares: list["Square"]) -> None:
        for i in range(len(squares)):
            other = squares[i]

            if other is self:
                continue

            if self.size <= other.size:
                continue

            if self.check_collision(other):
                squares[i] = Square(other.size)

    def apply_jitter(self) -> None:
        speed = math.hypot(self.dx, self.dy)
        angle = math.atan2(self.dy, self.dx)
        angle += random.uniform(-ANGLE_JITTER, ANGLE_JITTER)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def limit_speed(self) -> None:
        speed = math.hypot(self.dx, self.dy)
        if speed > self.max_speed and speed != 0:
            scale = self.max_speed / speed
            self.dx *= scale
            self.dy *= scale

    def flee(self, squares: list["Square"]) -> None:
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

    def chase(self, squares: list["Square"]) -> None:
        for other in squares:
            if other is self:
                continue
            if self.size <= other.size:
                continue

            diff_x = other.center_x() - self.center_x()
            diff_y = other.center_y() - self.center_y()
            distance = math.hypot(diff_x, diff_y)

            if distance < CHASE_DISTANCE:
                if diff_x > 0:
                    self.dx += CHASE_FORCE
                else:
                    self.dx -= CHASE_FORCE

                if diff_y > 0:
                    self.dy += CHASE_FORCE
                else:
                    self.dy -= CHASE_FORCE

    def move(self, squares: list["Square"], dt: float) -> None:
        self.apply_jitter()
        self.flee(squares)
        self.chase(squares)
        self.limit_speed()

        self.x += self.dx * dt * FPS
        self.y += self.dy * dt * FPS

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

    def draw(self, screen: pygame.Surface) -> None:
        brightness = 1 - (self.age / self.life_span)

        if brightness < MIN_BRIGHTNESS:
            brightness = MIN_BRIGHTNESS

        red = int(self.color[0] * brightness)
        green = int(self.color[1] * brightness)
        blue = int(self.color[2] * brightness)

        pygame.draw.rect(
            screen,
            (red, green, blue),
            (int(self.x), int(self.y), self.size, self.size),
        )


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    squares: list[Square] = []

    for _ in range(BIG_SQUARES):
        squares.append(Square(BIG_SIZE))

    for _ in range(MEDIUM_SQUARES):
        squares.append(Square(MEDIUM_SIZE))

    for _ in range(SMALL_SQUARES):
        squares.append(Square(SMALL_SIZE))

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
                squares[i] = Square(squares[i].size)

            squares[i].move(squares, dt)
            squares[i].eat(squares)
            squares[i].draw(screen)

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
    