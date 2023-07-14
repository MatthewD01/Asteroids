import pygame
import numpy as np
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


class Ship:
    def __init__(self):
        self.dt = pygame.time.Clock().tick(60) / 5
        self.player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = pygame.Vector2(0, 1)
        self.rotation_speed = self.dt

    def translate_forward(self):
        self.player_pos = self.player_pos + (self.player_direction / 2)

    def rotate_clockwise(self):
        self.player_direction.rotate_ip(self.rotation_speed)

    def rotate_anticlockwise(self):
        self.player_direction.rotate_ip(-self.rotation_speed)

    def render(self, screen):
        front = self.player_pos + self.player_direction * 10
        middle = self.player_pos - (self.player_direction * 5)
        back_left = self.player_pos + (self.player_direction.rotate(-130) * 10)
        back_right = self.player_pos + (self.player_direction.rotate(130) * 10)
        self.ship_coords = (front, back_left, middle, back_right)
        pygame.draw.polygon(screen, "white", (self.ship_coords))


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 0.001
        pygame.sprite.Sprite.__init__(self)

    def spawn(self):
        top_border_region = (random.randint(0, WINDOW_WIDTH), -20)
        left_border_region = (-20, random.randint(0, WINDOW_HEIGHT))
        bottom_border_region = (random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT + 20)
        right_border_region = (WINDOW_WIDTH + 20, random.randint(0, WINDOW_HEIGHT))
        coords = [
            top_border_region,
            left_border_region,
            bottom_border_region,
            right_border_region,
        ]
        choice = np.random.choice([0, 1, 2, 3])
        self.generator(coords[choice])

    def generator(self, spawn_coords):
        x_position, y_position = spawn_coords
        circle_resolution = np.linspace(0, 2 * np.pi, 50)
        self.size = 20
        self.circle = [
            (
                (
                    self.size * np.cos(circle_resolution) + np.random.normal(0, 1.2, 50)
                ).round(3)
            )
            + x_position,
            (
                (
                    self.size * np.sin(circle_resolution) + np.random.normal(0, 1, 50)
                ).round(3)
            )
            + y_position,
        ]
        self.spawned_asteroid = list(zip(self.circle[0], self.circle[1]))

    def initial_direction(self, player_position):
        self.asteroid_direction = (
            pygame.Vector2(*self.spawned_asteroid[0]) - player_position
        ) * self.speed

    def render(self, screen):
        self.spawned_asteroid = [
            pygame.Vector2(
                (x - self.asteroid_direction[0]), (y - self.asteroid_direction[1])
            )
            for x, y in self.spawned_asteroid
        ]
        pygame.draw.polygon(screen, "white", self.spawned_asteroid)


def main():
    pygame.init()
    timer = 0
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = True
    paused = True
    clock = pygame.time.Clock()
    ship, asteroid = Ship(), Asteroid()
    onscreen_asteroids = pygame.sprite.Group()
    onscreen_asteroids.add(Asteroid())
    onscreen_asteroids.add(Asteroid())
    print(onscreen_asteroids.sprites)
    asteroid.spawn()
    asteroid.initial_direction(ship.player_pos)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.K_ESCAPE:
                paused = not paused
        screen.fill("Black")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            ship.translate_forward()
        if keys[pygame.K_d]:
            ship.rotate_clockwise()
        if keys[pygame.K_a]:
            ship.rotate_anticlockwise()

        ship.render(screen)
        onscreen_asteroids.draw(screen)
        pygame.display.flip()
        timer += 1
        if timer % 5000 == 0:
            print(timer % 5000)
            spawn

        clock.tick(60)


def spawn(asteroid):
    print("spawn")


if __name__ == "__main__":
    main()
