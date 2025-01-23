import random
import math

import pygame
from pygame.math import Vector2

from constants import PIXELS_PER_METER, HEIGHT, WIDTH

class Drone:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.speed = 10  # Constant speed for movement

        self.color = (0, 0, 0)  # Black color for the drone
        self.width = 20  # Width of the drone
        self.height = 10  # Height of the drone

        self.rect = self._set_rect()  # Initialize the rect for collision checking

    def update(self, dt, wind):
        # Movement controls based on arrow keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.position.x -= self.speed * dt  # Move left
        if keys[pygame.K_RIGHT]:
            self.position.x += self.speed * dt  # Move right

        # Prevent the drone from going off-screen
        self.position.x = max(0, min(self.position.x, WIDTH))
        # Update the rect position to match the new position
        self.rect = self._set_rect()

    def render(self, screen):
        # Convert position to pixels for rendering
        position_pixels = self.position * PIXELS_PER_METER
        pygame.draw.rect(
            screen, self.color,
            pygame.Rect(
                position_pixels.x - self.width // 2,  # Center the rectangle
                position_pixels.y - self.height // 2,  # Center the rectangle
                self.width, self.height
            )
        )

    def _set_rect(self):
        return pygame.Rect(
            self.position.x * PIXELS_PER_METER - self.width // 2,
            self.position.y * PIXELS_PER_METER - self.height // 2,
            self.width, self.height
        )

