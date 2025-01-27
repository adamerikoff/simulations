import pygame

from utils import Vector
from entities.grenade import Grenade

class Drone:
    def __init__(self, x, y, width=5, height=2):
        """
        Initialize the drone.

        Args:
            x (float): Initial x-coordinate in meters.
            y (float): Initial y-coordinate in meters.
            width (float): Width of the drone in meters (default: 2 meters).
            height (float): Height of the drone in meters (default: 1 meter).
        """
        self.coordinates = Vector(x, y)  # Position of the drone (top-left corner)
        self.width = width  # Width of the drone in meters
        self.height = height  # Height of the drone in meters
        self.grenade = None

    def update(self, action, dt):
        """
        Update the drone's position based on the action and time step.
        
        Args:
            action (str): Action to be performed ("right", "left", "drop").
            dt (float): Time step for the update.
        """
        if not self.grenade.released:
            if action == 0:
                self.coordinates.x += 10 * dt  # Move right
                self.grenade.coordinates.x = self.coordinates.x
                self.grenade.coordinates.y = self.coordinates.y + 1
            elif action == 1:
                self.coordinates.x -= 10 * dt  # Move left
                self.grenade.coordinates.x = self.coordinates.x
                self.grenade.coordinates.y = self.coordinates.y + 1
            elif action == 2:
                self.grenade.released = True
            else:
                pass

    def attach_grenade(self):
        self.grenade = Grenade(self.coordinates.x, self.coordinates.y + 1)
        return self.grenade

    def render(self, screen, pixel_per_meter):
        """
        Render the drone as a rectangle on the screen.
        
        Args:
            screen (pygame.Surface): The Pygame screen to render on.
            pixel_per_meter (int): Conversion factor from meters to pixels.
        """
        # Convert world coordinates and dimensions to screen coordinates
        screen_x = int((self.coordinates.x - self.width / 2) * pixel_per_meter)
        screen_y = int((self.coordinates.y - self.height / 2) * pixel_per_meter)
        screen_width = int(self.width * pixel_per_meter)
        screen_height = int(self.height * pixel_per_meter)

        # Draw the drone as a rectangle
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, screen_width, screen_height))
