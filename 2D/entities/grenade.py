import pygame

from constants import GRAVITY, PIXELS_PER_METER, HEIGHT, WIDTH

class Grenade:
    def __init__(self, x, y):
        self.x = x  # Position in meters
        self.y = y  # Position in meters
        self.radius = 1  # Radius in meters
        self.fake_radius = 5  # Fake radius for rendering in pixels
        self.color = (255, 0, 0)  # Red color
        self.velocity = 0  # Initial velocity
        self.rect = self._set_rect()  # Initialize the rect for collision checking

    def update(self, dt):
        # Update velocity and position based on gravity
        self.velocity += GRAVITY * dt
        self.y += self.velocity * dt  # Update y position based on velocity

        # Collision check with the bottom of the screen (in meters)
        if self.y >= HEIGHT:
            self.y = HEIGHT  # Make sure grenade doesn't go below the ground level
            self.velocity = 0  # Stop velocity after hitting the ground
        
        self.rect = self._set_rect()  # Update the rect position to match the new y

    def render(self, screen):
        # Convert the position to pixels for rendering
        y_pixels = int(self.y * PIXELS_PER_METER)
        x_pixels = int(self.x * PIXELS_PER_METER)
        pygame.draw.circle(screen, self.color, (x_pixels, y_pixels), self.fake_radius)

    def _set_rect(self):
        # Create a rect in pixels for collision detection (without converting to pixels each time)
        return pygame.Rect(
            self.x * PIXELS_PER_METER - self.radius,
            self.y * PIXELS_PER_METER - self.radius,
            self.radius * 2,
            self.radius * 2
        )
