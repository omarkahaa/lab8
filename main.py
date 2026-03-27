import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab 8 - Moving Squares")

WHITE = (255, 255, 255)

clock = pygame.time.Clock()


class Square:
    def __init__(self):
        self.size = 30
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )
        self.dx = random.choice([-3, -2, -1, 1, 2, 3])
        self.dy = random.choice([-3, -2, -1, 1, 2, 3])

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.dx *= -1

        if self.y <= 0 or self.y >= HEIGHT - self.size:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


def main():
    squares = [Square() for _ in range(10)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares:
            square.move()

        SCREEN.fill(WHITE)

        for square in squares:
            square.draw(SCREEN)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()
