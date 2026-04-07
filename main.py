import math
import random

import pygame

WIDTH = 800
HEIGHT = 600
NUM_SQUARES = 100
MIN_SIZE = 10
MAX_SIZE = 40
GLOBAL_MAX_SPEED = 6
ANGLE_JITTER = 0.15
BACKGROUND_COLOR = (255, 255, 255)
FPS = 60

FLEE_DISTANCE = 100
FLEE_FORCE = 0.2


class Square:
    def __init__(self):
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

    def center_x(self):
        return self.x + self.size / 2

    def center_y(self):
        return self.y + self.size / 2

    def apply_jitter(self):
        speed = math.hypot(self.dx, self.dy)
        angle = math.atan2(self.dy, self.dx)

        angle += random.uniform(-ANGLE_JITTER, ANGLE_JITTER)

        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def limit_speed(self):
        speed = math.hypot(self.dx, self.dy)
        if speed > self.max_speed and speed != 0:
            scale = self.max_speed / speed
            self.dx *= scale
            self.dy *= scale

    def flee(self, squares):
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

    def move(self, squares):
        self.apply_jitter()
        self.flee(squares)
        self.limit_speed()

        self.x += self.dx
        self.y += self.dy

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

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (int(self.x), int(self.y), self.size, self.size),
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    squares = [Square() for _ in range(NUM_SQUARES)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for square in squares:
            square.move(squares)
            square.draw(screen)

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()