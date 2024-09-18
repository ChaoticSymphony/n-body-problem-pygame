import pygame
import math
import numpy as np

a = 80
vel = 0.5

red = (193, 81, 81)
cyan = (85, 209, 209)
blue = (85, 100, 209)
white = (255, 255, 255)
pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Solar System")

class Body:
    G = 1  # Gravitational constant
    radius = 9  # Default radius for drawing planets

    def __init__(self, mass, color, x, y, vx, vy):
        self.mass = mass
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.orbit = []

    def draw_orbit(self, screen, offset_x, offset_y):
        if len(self.orbit) > 1:
            max_thickness_distance = 20  # Distance after which the thickness should taper to 1px
            for i in range(1, len(self.orbit)):
                start_pos = (self.orbit[i - 1][0] + offset_x, self.orbit[i - 1][1] + offset_y)
                end_pos = (self.orbit[i][0] + offset_x, self.orbit[i][1] + offset_y)
                
                if i < max_thickness_distance:
                    thickness = 2
                    if i < max_thickness_distance / 2:
                        thickness = 1
                else:
                    thickness = 3

                pygame.draw.line(screen, self.color, start_pos, end_pos, thickness)

    def draw_planet(self, screen, offset_x, offset_y):
        # Create a surface with transparency to draw the glow
        glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)

        # Define maximum radius for the glow
        max_radius = 36  
        steps = 36  # Number of concentric circles for the gradient glow

        for i in range(steps):
            radius = max_radius - (i * max_radius // steps)
            alpha = 0 + (i * 100 // steps)
            glow_color = (self.color[0], self.color[1], self.color[2], alpha)
            pygame.draw.circle(glow_surface, glow_color, (50, 50), radius)

        # Blit the glow surface onto the screen, centering it around the planet
        screen.blit(glow_surface, (int(self.x + offset_x - 50), int(self.y + offset_y - 50)))

        # Draw the planet itself
        pygame.draw.circle(screen, self.color, (int(self.x + offset_x), int(self.y + offset_y)), self.radius)

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
        if len(self.orbit) > 100:  # Keep the orbit list from growing indefinitely
            self.orbit.pop(0)

    def interact_with(self, other):
        self.accelerate_due_to_gravity(other)
        other.accelerate_due_to_gravity(self)

    def check_collision(self, other):
        # Calculate the distance between the two planets
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # If the distance is less than the sum of their radii, they have collided
        return distance <= (self.radius + other.radius-3)

    @staticmethod
    def merge_planets(body1, body2):
        # Calculate the new mass
        new_mass = body1.mass + body2.mass

        # Calculate the resultant velocity using conservation of momentum
        new_vx = (body1.vx * body1.mass + body2.vx * body2.mass) / new_mass
        new_vy = (body1.vy * body1.mass + body2.vy * body2.mass) / new_mass

        # Calculate the position of the new planet (weighted by mass)
        new_x = (body1.x * body1.mass + body2.x * body2.mass) / new_mass
        new_y = (body1.y * body1.mass + body2.y * body2.mass) / new_mass

        # Average the colors to get a blended color
        new_color = (
            (body1.color[0] + body2.color[0]) // 2,
            (body1.color[1] + body2.color[1]) // 2,
            (body1.color[2] + body2.color[2]) // 2,
        )

        # Create the new merged planet
        new_body = Body(mass=new_mass, color=new_color, x=new_x, y=new_y, vx=new_vx, vy=new_vy)

        return new_body


running = True
clock = pygame.time.Clock()

# Pan variables
pan_offset_x = 0
pan_offset_y = 0
dragging = False
last_mouse_pos = None

sides = -0.5
centre = sides*2
y_off = 20
x_off = 20

bodies = [
    Body(mass=a, color=red, x=750, y=400, vx=-centre, vy=-centre),
    Body(mass=a, color=cyan, x=700, y=400+y_off, vx=sides, vy=sides),
    Body(mass=a, color=blue, x=800, y=400-y_off, vx=sides, vy=sides),
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

    # Check for collisions and merge planets if necessary
    merged_bodies = []
    i = 0
    while i < len(bodies):
        j = i + 1
        while j < len(bodies):
            if bodies[i].check_collision(bodies[j]):
                # Merge the two colliding planets and replace them with the new body
                new_body = Body.merge_planets(bodies[i], bodies[j])
                merged_bodies.append(new_body)
                bodies.pop(j)  # Remove the second body
                bodies.pop(i)  # Remove the first body
                i -= 1  # Decrement i to ensure we process correctly after removing
                break
            j += 1
        i += 1

    # Add the new merged bodies to the list
    bodies.extend(merged_bodies)

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
