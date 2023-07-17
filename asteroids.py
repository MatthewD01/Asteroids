import pygame
import numpy as np
import random


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        self.dt = pygame.time.Clock().tick(60) / 5
        self.player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = pygame.Vector2(0, 1)
        self.rotation_speed = self.dt
        super().__init__()

    def translate_forward(self):
        self.player_pos = self.player_pos + (self.player_direction / 1.5)

    def rotate_clockwise(self):
        self.player_direction.rotate_ip(self.rotation_speed)

    def rotate_anticlockwise(self):
        self.player_direction.rotate_ip(-self.rotation_speed)

    def render(self, screen):
        front = self.player_pos + self.player_direction * 10
        middle = self.player_pos - (self.player_direction * 5)
        back_left = self.player_pos + (self.player_direction.rotate(-130) * 10)
        back_right = self.player_pos + (self.player_direction.rotate(130) * 10)
        self.coordinates = [front, back_left, middle, back_right]
        self.rect = pygame.draw.polygon(screen, "white", (self.coordinates))


class Laser(pygame.sprite.Sprite):
    def __init__(self, player_position, player_direction) -> None:
        self.speed = 0.1
        # self.corners = [(0, 0), (0, 10), (2, 10), (2, 0)]
        x, y = player_position
        self.direction_x, self.direction_y = player_direction * 10
        self.projectile = pygame.Rect(x - 1, y, 2, 10)

        print(f"projectile {self.projectile}")
        super().__init__()

    def update(self, screen):
        self.projectile.move(self.direction_x, self.direction_y)
        pygame.draw.rect(screen, "red", self.projectile)


class Boundaries(pygame.sprite.Sprite):
    def __init__(self, screen):
        offset = 50
        top_left = (-offset, -offset)
        top_right = (WINDOW_WIDTH + offset, -offset)
        bottom_left = (-offset, WINDOW_HEIGHT + offset)
        bottom_right = (WINDOW_WIDTH + offset, WINDOW_HEIGHT + offset)
        self.coordinates = [top_left, top_right, bottom_right, bottom_left]
        left = pygame.Rect(-offset, -offset, 1, WINDOW_HEIGHT + offset)
        top = pygame.Rect(-offset, -offset, WINDOW_WIDTH + offset, 1)
        right = pygame.Rect(WINDOW_WIDTH + offset, -offset, -1, WINDOW_HEIGHT + offset)
        bottom = pygame.Rect(-offset, WINDOW_HEIGHT + offset, WINDOW_WIDTH + offset, -1)
        self.rect = pygame.Rect.unionall(left, [top, right, bottom])
        pygame.draw.rect(screen, "red", self.rect)
        super().__init__()

    def update(self, screen):
        self.rect = pygame.draw.polygon(screen, "red", self.coordinates, width=2)


class LeftBoundary(pygame.sprite.Sprite):
    def __init__(self, offset) -> None:
        self.rect = pygame.Rect(-offset, -offset, 1, WINDOW_HEIGHT + offset)
        super().__init__()


class TopBoundary(pygame.sprite.Sprite):
    def __init__(self, offset: int):
        self.rect = pygame.Rect(-offset, -offset, WINDOW_WIDTH + offset, 1)
        super().__init__()


class RightBoundary(pygame.sprite.Sprite):
    def __init__(self, offset: int):
        self.rect = pygame.Rect(
            -offset, WINDOW_HEIGHT + offset, WINDOW_WIDTH + offset, -1
        )
        super().__init__()


class BottomBoundary(pygame.sprite.Sprite):
    def __init__(self, offset):
        self.rect = pygame.Rect(
            -offset, WINDOW_HEIGHT + offset, WINDOW_WIDTH + offset, -1
        )
        super().__init__()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, player_position: Ship):
        self.speed = random.randint(1, 5) / 1000
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.spawn()
        self.initial_direction(player_position)
        super().__init__()

    def spawn(self):
        offset = 30
        top_border_region = (random.randint(0, WINDOW_WIDTH), -offset)
        left_border_region = (-offset, random.randint(0, WINDOW_HEIGHT))
        bottom_border_region = (random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT + offset)
        right_border_region = (WINDOW_WIDTH + offset, random.randint(0, WINDOW_HEIGHT))
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
        self.size = random.choice([10, 15, 20, 30])
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

    def update(self, screen):
        self.spawned_asteroid = [
            pygame.Vector2(
                (x - self.asteroid_direction[0]), (y - self.asteroid_direction[1])
            )
            for x, y in self.spawned_asteroid
        ]
        self.rect = pygame.draw.polygon(screen, "white", self.spawned_asteroid)


def main():
    pygame.init()
    timer = 0
    offset = 50
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = True
    clock = pygame.time.Clock()
    ship = Ship()
    asteroids = pygame.sprite.Group()
    # boundary.update(screen)
    lasers = pygame.sprite.Group()
    asteroids.add(Asteroid(ship.player_pos), Asteroid(ship.player_pos))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("Black")
        ship.render(screen)
        lasers.update(screen)
        asteroids.update(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            ship.translate_forward()
        if keys[pygame.K_d]:
            ship.rotate_clockwise()
        if keys[pygame.K_a]:
            ship.rotate_anticlockwise()
        # if keys[pygame.K_SPACE]:
        #     lasers.add(Laser(ship.player_pos, ship.player_direction))

        timer += 1
        if timer % (random.choice([50, 100, 200, 300, 500])) == 0:
            asteroids.add(Asteroid(ship.player_pos))
        if pygame.sprite.spritecollideany(ship, asteroids):
            game_over()
            break
        asteroids.remove(boundary_check(asteroids, offset))
        print(len(asteroids.sprites()))
        clock.tick(60)
        pygame.display.flip()


def game_over():
    print("game over")

    """ + 100 for each asteroid
    every 1000 points -> timer % decrease 50
    """


def boundary_check(asteroids, offset):
    new_asteroids = asteroids.sprites()
    remove_asteroids = []
    for asteroid in new_asteroids:
        x_coord, y_coord, _, _ = asteroid.rect
        if -offset < x_coord < WINDOW_WIDTH + offset:
            pass
        elif -offset < y_coord < WINDOW_HEIGHT + offset:
            pass
        else:
            remove_asteroids.append(asteroid)

    return remove_asteroids


if __name__ == "__main__":
    main()
