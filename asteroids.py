import pygame 
import numpy as np
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

class Ship():
    def __init__(self):
        self.dt = pygame.time.Clock().tick(60) / 1000 
        self.player_pos = pygame.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.player_direction = pygame.Vector2(0,1)
        self.rotation_speed = self.dt * 8  
    def translate_forward(self):
        self.player_pos = self.player_pos + (self.player_direction / 15)
    def rotate_clockwise(self):
        self.player_direction.rotate_ip(self.rotation_speed)
    def rotate_anticlockwise(self):
        self.player_direction.rotate_ip(-self.rotation_speed)  
    def ship_draw(self, screen):
        front = self.player_pos + self.player_direction * 10 
        middle = self.player_pos - (self.player_direction * 5)
        back_left = self.player_pos + (self.player_direction.rotate(-130) * 10)
        back_right = self.player_pos + (self.player_direction.rotate(130) * 10)
        self.ship_coords = (front, back_left, middle, back_right)
        pygame.draw.polygon(screen, "white", (self.ship_coords))
        
class projectile():
    ...
    
class Asteroids():
    def spawn(self):
        top_border_region = (random.randint(0,WINDOW_WIDTH), -20)
        left_border_region = (-20, random.randint(0, WINDOW_HEIGHT))
        bottom_border_region = (random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT+20)
        right_border_region = (WINDOW_WIDTH + 20, random.randint(0, WINDOW_HEIGHT))
        coords_list = [top_border_region, left_border_region, bottom_border_region, right_border_region]
        choice = np.random.choice([0,1,2,3])
        self.asteroid_generator(coords_list[choice])
        
        
    def asteroid_generator(self, spawn_coords):
        x_position, y_position = spawn_coords
        circle_resolution = np.linspace(0, 2 * np.pi, 50)
        size = 20
        self.circle = [
            ((size * np.cos(circle_resolution) + np.random.normal(0,1.2,50)).round(3)) + x_position,
            ((size * np.sin(circle_resolution) + np.random.normal(0,1,50)).round(3)) + y_position
            ]
        self.spawned = list(zip(self.circle[0], self.circle[1]))
        
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.spawned)
    def move():
        ...
        
    def is_hit():
        ...
    
    def initial_direction():
        #generated position towards the player?
        #create a vector going towards it, keep it until asteroid dies
        ...
        
    
def main():
    pygame.init()
    ship, asteroids = Ship(), Asteroids()
    asteroids.spawn()
    clock = pygame.time.Clock()
    running = True
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    paused = True
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
     
        ship.ship_draw(screen)
        pygame.display.flip()

main()