import pygame
from pygame.math import Vector2

from constants import PIXELS_PER_METER, HEIGHT, WIDTH

class Enemy:
    def __init__(self, x):
        # Randomly spawn the enemy at the bottom of the screen
        self.position = Vector2(x, HEIGHT)  # 30 is the height offset
        self.color = (255, 105, 180)  # Pink color
        self.size = 20  # Size of the enemy square

        self.rect = self._set_rect()  # Initialize the rect for collision checking

    def update(self):
        pass

    def render(self, screen):
        # Convert position to pixels for rendering
        position_pixels = self.position * PIXELS_PER_METER
        pygame.draw.rect(
            screen, self.color,
            pygame.Rect(
                position_pixels.x - self.size // 2,  # Center the square
                position_pixels.y - self.size // 2,  # Center the square
                self.size, self.size
            )
        )

    def _set_rect(self):
        return pygame.Rect(
            self.position.x * PIXELS_PER_METER - self.size // 2,
            self.position.y * PIXELS_PER_METER - self.size // 2,
            self.size, self.size
        )
