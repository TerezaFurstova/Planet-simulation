import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)

class Object:
    AU = 149.6e9 # distance Earth - Sun in meters
    G = 6.67328e-11
    SCALE = 250 / AU   # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # seconds in one day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x,y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x   # ???
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 + distance_y **2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass *other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, objects):
        total_fx = total_fy = 0
        for object in objects:
            if self == object:
                continue

            fx, fy = self.attraction(object)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
       

def main():
    run = True
    clock = pygame.time.Clock()
 
    sun = Object(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Object(Object.AU, 0, 16, BLUE, 5.97219 * 10**24)
    earth.y_vel = 29.783*1000

    moon = Object(Object.AU + earth.radius + 6371000 + 384400000, 0, 6, WHITE, 7.34767*10**22)
    moon.y_vel = 30*1000

    objects = [sun, earth, moon]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # we hit x-button in the window
                run = False
        
        for object in objects:
            object.update_position(objects)
            object.draw(WIN)
        
        pygame.display.update()
    
    pygame.quit()

main()
