import pygame
import numpy as np
import random
import time
import sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FIRE_INTERVAL = 1


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        self.dt = pygame.time.Clock().tick(60) / 5
        self.player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = pygame.Vector2(0, 1)
        self.rotation_speed = self.dt
        super().__init__()

    def translate_forward(self) -> None:
        self.player_pos = self.player_pos + (self.player_direction / 1.5)

    def rotate_clockwise(self) -> None:
        self.player_direction.rotate_ip(self.rotation_speed)

    def rotate_anticlockwise(self) -> None:
        self.player_direction.rotate_ip(-self.rotation_speed)

    def update(self, screen: pygame.display) -> None:
        front = self.player_pos + self.player_direction * 10
        middle = self.player_pos - (self.player_direction * 5)
        back_left = self.player_pos + (self.player_direction.rotate(-130) * 10)
        back_right = self.player_pos + (self.player_direction.rotate(130) * 10)
        self.coordinates = [front, back_left, middle, back_right]
        self.rect = pygame.draw.polygon(screen, "white", (self.coordinates))


class Laser(pygame.sprite.Sprite):
    def __init__(
        self, player_position: pygame.Vector2, player_direction: pygame.Vector2
    ) -> None:
        self.speed = 0.3
        self.direction = player_direction
        self.pos = player_position
        bottom_right = player_position + self.direction.rotate(90)
        top_right = player_position + self.direction.rotate(5) * 20
        top_left = player_position + self.direction.rotate(-5) * 20
        bottom_left = player_position + self.direction.rotate(-90)
        self.corners = [bottom_right, top_right, top_left, bottom_left]
        self.start = self.pos + self.direction * 10
        self.end = self.pos + self.direction * 20
        super().__init__()

    def update(self, screen: pygame.display) -> None:
        self.start += self.direction
        self.end += self.direction
        self.rect = pygame.draw.line(screen, "red", self.start, self.end, width=4)


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

    def generator(self, spawn_coords: tuple) -> None:
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

    def initial_direction(self, player_position: pygame.Vector2) -> None:
        self.asteroid_direction = (
            pygame.Vector2(*self.spawned_asteroid[0]) - player_position
        ) * self.speed

    def update(self, screen: pygame.display) -> None:
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
    running = True
    game_ended = False
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    ship = Ship()
    asteroids = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    total_score = 0
    score_check = True
    last_time_fired = time.time()

    asteroid_interval = [50, 100, 200, 300]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not game_ended:
            screen.fill("Black")
            ship.update(screen)
            asteroids.update(screen)
            lasers.update(screen)
            score(screen, total_score)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                ship.translate_forward()
            if keys[pygame.K_d]:
                ship.rotate_clockwise()
            if keys[pygame.K_a]:
                ship.rotate_anticlockwise()
            if keys[pygame.K_SPACE]:
                if time.time() - last_time_fired >= FIRE_INTERVAL:
                    lasers.add(Laser(ship.player_pos, ship.player_direction.copy()))
                    lasers.update(screen)
                    last_time_fired = time.time()

            timer += 1
            if timer % (random.choice(asteroid_interval)) == 0:
                asteroids.add(Asteroid(ship.player_pos))

            if pygame.sprite.spritecollideany(ship, asteroids):
                game_ended = True

            if pygame.sprite.groupcollide(
                lasers, asteroids, dokilla=True, dokillb=True
            ):
                total_score += 100

            asteroids.remove(boundary_check(asteroids, offset))
            lasers.remove(boundary_check(lasers, offset))
            print(f"score {total_score}")
            print(total_score % 500)
            asteroid_interval, score_check = score_increase(
                total_score, asteroid_interval, score_check
            )
        elif game_ended:
            game_over(screen)
            try_again(screen)
        clock.tick(60)
        pygame.display.flip()


def boundary_check(object_group: pygame.sprite.Group, offset: int) -> list:
    objects = object_group.sprites()
    remove_objects = []
    for object in objects:
        x_coord, y_coord, _, _ = object.rect
        if -offset < x_coord < WINDOW_WIDTH + offset:
            pass
        elif -offset < y_coord < WINDOW_HEIGHT + offset:
            pass
        else:
            remove_objects.append(object)

    return remove_objects


def game_over(display: pygame.display) -> True:
    font = pygame.font.Font("VT323-Regular.ttf", 64)
    text = font.render("GAME OVER", True, "red")
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    display.blit(text, text_rect)
    return True


def font(size: int, font_name: str, phrase: str, colour: str) -> list:
    used_font = pygame.font.Font(font_name, size)
    text = used_font.render(f"{phrase}", True, colour)
    text_rect = text.get_rect()
    return [text, text_rect]


def score(display: pygame.display, total_score: int) -> None:
    text, text_rect = font(32, "VT323-Regular.ttf", total_score, "red")
    text_rect.center = (42, 42)
    display.blit(text, text_rect)


def score_increase(
    total_score: int, asteroid_interval: list, score_check: bool
) -> list:
    # print(f"score {total_score}")
    # print(total_score % 500)
    if total_score % 500 == 0 and total_score != 0 and score_check:
        asteroid_interval = [interval * 1.02 for interval in asteroid_interval]
        score_check = False
        print(asteroid_interval)
    if total_score % 500 != 0:
        score_check = True
    return asteroid_interval, score_check


def try_again(display):
    text, text_rect = font(20, "VT323-Regular.ttf", "Try again(Y/N)", "red")
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5)
    display.blit(text, text_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_y]:
        main()
    elif keys[pygame.K_n]:
        sys.exit()


if __name__ == "__main__":
    main()
