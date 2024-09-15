import pygame
import math
import numpy as np

a = 100
vel = 1

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Solar System")

class Body:
    G = 1  # Gravitational constant

    def __init__(self, mass, color, x, y, vx, vy):
        self.mass = mass
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.orbit = []

    def draw_orbit(self, screen, offset_x, offset_y):
        # Draw the orbit with an offset
        if len(self.orbit) > 1:
            adjusted_orbit = [(x + offset_x, y + offset_y) for x, y in self.orbit]
            pygame.draw.lines(screen, self.color, False, adjusted_orbit, 1)

    def draw_planet(self, screen, offset_x, offset_y):
        # Draw the body itself with an offset
        pygame.draw.circle(screen, self.color, (int(self.x + offset_x), int(self.y + offset_y)), 9)

    def accelerate_due_to_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        d = math.sqrt(dx**2 + dy**2)
        if d == 0:
            return  # Avoid division by zero
        f = self.G * self.mass * other.mass / d**2
        ax = f * dx / d / self.mass
        ay = f * dy / d / self.mass
        self.vx += ax
        self.vy += ay

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 1200:  # Keep the orbit list from growing indefinitely
            self.orbit.pop(0)

    def interact_with(self, other):
        self.accelerate_due_to_gravity(other)
        other.accelerate_due_to_gravity(self)

running = True
clock = pygame.time.Clock()

# Pan variables
pan_offset_x = 0
pan_offset_y = 0
dragging = False
last_mouse_pos = None

bodies = [
    Body(mass=a, color=(193, 81, 81), x=750, y=400, vx=-0.5, vy=-0.5),
    Body(mass=a, color=(85, 209, 209), x=600, y=400, vx=0.5, vy=0.5),
    Body(mass=5, color=(85, 100, 209), x=900, y=400, vx=-0., vy=0.),
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if last_mouse_pos:
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    pan_offset_x += dx
                    pan_offset_y += dy
                    last_mouse_pos = (mouse_x, mouse_y)

    screen.fill("black")

    # Loop through each pair of bodies to calculate interactions
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            bodies[i].interact_with(bodies[j])

    # Move each body first
    for body in bodies:
        body.move()

    # Draw all orbits first
    for body in bodies:
        body.draw_orbit(screen, pan_offset_x, pan_offset_y)

    # Draw all planets
    for body in bodies:
        body.draw_planet(screen, pan_offset_x, pan_offset_y)

    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
