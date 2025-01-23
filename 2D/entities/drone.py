import random
import math

import pygame
from pygame.math import Vector2

from constants import PIXELS_PER_METER, HEIGHT, WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from entities import Grenade

class Drone:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.speed = 10  # Constant speed for movement

        self.color = (0, 0, 0)  # Black color for the drone
        self.width = 20  # Width of the drone
        self.height = 10  # Height of the drone

        self.rect = self._set_rect()  # Initialize the rect for collision checking

        self.grenade = Grenade(self.position.x, self.position.y)

    def update(self, dt, wind):
        # Movement controls based on arrow keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.position.x -= self.speed * dt  # Move left
            self.grenade.position.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.position.x += self.speed * dt  # Move right
            self.grenade.position.x += self.speed * dt
        if keys[pygame.K_DOWN]:
            self.grenade.released = True
            self.grenade_initial_pos = self.grenade.position.copy()
        # Prevent the drone from going off-screen
        self.position.x = max(0, min(self.position.x, WIDTH))
        self.grenade.position.x = max(0, min(self.grenade.position.x, WIDTH))
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
        if self.grenade.released:
            self._draw_straight_projectory(screen)

    def _draw_straight_projectory(self, screen):
        pygame.draw.line(
            screen, (0, 255, 0),
            (self.grenade_initial_pos.x * PIXELS_PER_METER, self.grenade_initial_pos.y * PIXELS_PER_METER),
            (self.grenade_initial_pos.x * PIXELS_PER_METER, SCREEN_HEIGHT), 
            1
        )

    def _set_rect(self):
        return pygame.Rect(
            self.position.x * PIXELS_PER_METER - self.width // 2,
            self.position.y * PIXELS_PER_METER - self.height // 2,
            self.width, self.height
        )

