import pygame
import random
import math

WIDTH = 800
HEIGHT = 600
NUM_SQUARES = 100
MIN_SIZE = 10
MAX_SIZE = 40
GLOBAL_MAX_SPEED = 6
JITTER_AMOUNT = 0.2
BACKGROUND_COLOR = (255, 255, 255)


class Square:
    def __init__(self):
        self.size = random.randint(MIN_SIZE, MAX_SIZE)
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

        self.max_speed = GLOBAL_MAX_SPEED * (MAX_SIZE / self.size)

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, min(self.max_speed, GLOBAL_MAX_SPEED))
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def apply_jitter(self):
        self.dx += random.uniform(-JITTER_AMOUNT, JITTER_AMOUNT)
        self.dy += random.uniform(-JITTER_AMOUNT, JITTER_AMOUNT)
        self.limit_speed()

    def limit_speed(self):
        speed = math.hypot(self.dx, self.dy)
        allowed_speed = min(self.max_speed, GLOBAL_MAX_SPEED)

        if speed > allowed_speed and speed != 0:
            scale = allowed_speed / speed
            self.dx *= scale
            self.dy *= scale

    def move(self):
        self.apply_jitter()

        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.dx *= -1
            self.x = max(0, min(self.x, WIDTH - self.size))

        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.dy *= -1
            self.y = max(0, min(self.y, HEIGHT - self.size))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.size, self.size))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()

    squares = [Square() for _ in range(NUM_SQUARES)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for square in squares:
            square.move()
            square.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()