import math

import pygame

from constants import GRAVITY, PIXELS_PER_METER, HEIGHT, WIDTH, AIR_DENSITY

class Grenade:
    def __init__(self, x, y):
        self.x = x  # Position in meters
        self.y = y  # Position in meters
        self.fake_radius = 5  # Fake radius for rendering in pixels
        self.color = (255, 0, 0)  # Red color
        self.velocity = 0  # Initial velocity
        
        self.radius = 0.032 #m
        self.mass = 0.4 #gramm
        self.drag_coefficient = 0.47  # Drag coefficient for a sphere
        self.cross_sectional_area = math.pi * (self.radius ** 2) #m^2
        self.terminal_velocity = self._calculate_terminal_velocity()

        self.rect = self._set_rect()  # Initialize the rect for collision checking

    def update(self, dt):
        gravitational_acceleration = GRAVITY
        drag_force = 0.5 * AIR_DENSITY * self.drag_coefficient * self.cross_sectional_area * (self.velocity ** 2)
        net_force = self.mass * gravitational_acceleration - drag_force
        acceleration = net_force / self.mass
        self.velocity += acceleration * dt
        if self.velocity > self.terminal_velocity:
            self.velocity = self.terminal_velocity

        self.y += self.velocity * dt

        if self.y >= HEIGHT:
            self.y = HEIGHT
            self.velocity = 0
        
        self.rect = self._set_rect()  # Update the rect position to match the new y

    def render(self, screen):
        # Convert the position to pixels for rendering
        y_pixels = int(self.y * PIXELS_PER_METER)
        x_pixels = int(self.x * PIXELS_PER_METER)
        pygame.draw.circle(screen, self.color, (x_pixels, y_pixels), self.fake_radius)

    def _calculate_terminal_velocity(self):
        return math.sqrt((2 * self.mass * GRAVITY) / (AIR_DENSITY * self.drag_coefficient * self.cross_sectional_area))


    def _set_rect(self):
        # Create a rect in pixels for collision detection (without converting to pixels each time)
        return pygame.Rect(
            self.x * PIXELS_PER_METER - 1,
            self.y * PIXELS_PER_METER - 1,
            2,
            2
        )
