import pygame
import math
import numpy as np

a = 1100 * math.pow(10, 12)
b = 1100 * math.pow(10, 12)
c = 300 * math.pow(10, 12)
vel = 11.2

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Solar System")

class Body:
    G = 6.67430 * math.pow(10, -11)  #Gravitational constant

    def __init__(self, mass, color, x, y, vx, vy):
        self.mass = mass
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.orbit = []

    def draw_orbit(self, screen):
        #Draws the orbit of the body first
        if len(self.orbit) > 1:
            pygame.draw.lines(screen, self.color, False, self.orbit, 1)
    def draw_planet(self, screen):
        #Draws the body itself
        pygame.draw.circle(screen, self.color, (float(self.x), float(self.y)), 10)

    def accelerate_due_to_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        d = math.sqrt(dx**2 + dy**2)
        if d == 0:
            return  #Avoid division by zero
        f = self.G * self.mass * other.mass / d**2
        ax = f * dx / d / self.mass
        ay = f * dy / d / self.mass
        self.vx += ax
        self.vy += ay

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 1200:  #Keep the orbit list from growing indefinitely
            self.orbit.pop(0)

    def interact_with(self, other):
        self.accelerate_due_to_gravity(other)
        other.accelerate_due_to_gravity(self)

running = True
clock = pygame.time.Clock()

bodies = [
    Body(mass=a, color=(193, 81, 81), x=700, y=350, vx=vel, vy=vel),
    Body(mass=b, color=(85, 209, 209), x=600, y=450, vx=-vel, vy=-vel),
    #Body(mass=c, color=(153, 255, 153), x=700, y=400, vx=1, vy=0.5),
    ]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    #Loop through each pair of bodies to calculate interactions
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            bodies[i].interact_with(bodies[j])
    #Move each body first
    for body in bodies:
        body.move()
    #Draw all orbits first
    for body in bodies:
        body.draw_orbit(screen)
    #Draw all planets
    for body in bodies:
        body.draw_planet(screen)   
    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS
pygame.quit()