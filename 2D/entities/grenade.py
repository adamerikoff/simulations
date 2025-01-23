import math

import pygame
from pygame.math import Vector2

from constants import GRAVITY, PIXELS_PER_METER, HEIGHT, WIDTH, AIR_DENSITY

class Grenade:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)

        self.fake_radius = 5
        self.color = (255, 0, 0)
        
        self.radius = 0.032  # m (radius in meters)
        self.mass = 0.4  # kg (mass in kilograms)
        self.drag_coefficient = 0.47  # Drag coefficient for a sphere
        self.cross_sectional_area = math.pi * (self.radius ** 2)  # m^2
        self.terminal_velocity = self._calculate_terminal_velocity()  # m/s

        self.rect = self._set_rect()  # Initialize the rect for collision checking


    def update(self, dt):
        # Forces: gravity and drag
        gravitational_force = Vector2(0, self.mass * GRAVITY)  # Gravity acts downward

        # Apply drag force only if the velocity is non-zero
        if self.velocity.length() > 0:
            drag_force = -0.5 * AIR_DENSITY * self.drag_coefficient * self.cross_sectional_area * self.velocity.length_squared() * self.velocity.normalize()  # Drag force (vector)
        else:
            drag_force = Vector2(0, 0)  # No drag force if no movement

        # Net force = gravity + drag force
        net_force = gravitational_force + drag_force

        # Acceleration = Net force / Mass
        acceleration = net_force / self.mass

        # Update velocity: velocity += acceleration * dt
        self.velocity += acceleration * dt

        # Cap velocity at terminal velocity
        if self.velocity.length() > self.terminal_velocity:
            self.velocity = self.velocity.normalize() * self.terminal_velocity

        # Update position: position += velocity * dt
        self.position += self.velocity * dt

        # Collision with the ground
        if self.position.y >= HEIGHT:
            self.position.y = HEIGHT
            self.velocity.y = 0  # Stop vertical velocity when hitting the ground

        # Update the rect position to match the new position
        self.rect = self._set_rect()


    def render(self, screen):
        # Convert position to pixels for rendering
        position_pixels = self.position * PIXELS_PER_METER
        pygame.draw.circle(
            screen, self.color, 
            (int(position_pixels.x), int(position_pixels.y)), 
            self.fake_radius
        )


    def _calculate_terminal_velocity(self):
        return math.sqrt(
            (2 * self.mass * GRAVITY) / 
            (AIR_DENSITY * self.drag_coefficient * self.cross_sectional_area)
            )



    def _set_rect(self):
        return pygame.Rect(
            self.position.x * PIXELS_PER_METER - 1,
            self.position.y * PIXELS_PER_METER - 1,
            2,
            2
        )
