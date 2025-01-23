import random
import math

import pygame
from pygame.math import Vector2

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, PIXELS_PER_METER, WIDTH, HEIGHT
from entities import Grenade


class Environment:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Free Fall Simulation")
        # Set the clock for managing the frame rate
        self.clock = pygame.time.Clock()
        # Set the background color (light grey)
        self.background_color = (200, 200, 200)
        # Set the font for text
        self.font = pygame.font.SysFont(None, 20)
        # Time tracking
        self.time_elapsed = 0  # Total time in seconds

        self.wind = self._generate_wind()
        self.entities = self._initialize_entities()

    def update(self):
        dt = self.clock.tick(FPS) / 1000.0
        self.time_elapsed += dt
        for entity in self.entities:
            entity.update(dt, self.wind)

    def render(self):
        """Render all elements to the screen."""
        # Fill the screen with the background color
        self.screen.fill(self.background_color)
        self._draw_info()
        for entity in self.entities:
            entity.render(self.screen)

    def run(self):
        """Main loop for the environment."""
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Update the environment
            self.update()
            # Render the environment
            self.render()
            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            self.clock.tick(FPS)

        # Quit Pygame
        pygame.quit()

    def _generate_wind(self):
        wind_speed = pygame.math.Vector2(random.uniform(-35, 35), 0)
        return wind_speed

    def _initialize_entities(self):
        entities = []
        entities.append(Grenade(WIDTH // 2, 10))
        return entities

    def _draw_scale(self):
        for y in range(0, HEIGHT+20, 20):
            text = self.font.render(f"{y} meters", True, (0, 0, 0))
            self.screen.blit(text, (5, SCREEN_HEIGHT-(y*5)))

    def _draw_time_counter(self):
        time_text = f"Time: {self.time_elapsed:.2f} s"
        text = self.font.render(time_text, True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 150, 10))

    def _draw_grenade_velocity(self):
        grenade = self.entities[0]
        # Get the magnitude (speed) of the velocity vector
        velocity_magnitude = grenade.velocity.length()  # This gives the speed as a scalar value (m/s)
        # Create the text to display the current velocity and terminal velocity
        velocity_text = f"Velocity: {velocity_magnitude:.2f} m/s"
        terminal_velocity_text = f"T.Velocity: {grenade.terminal_velocity:.2f} m/s"        
        # Render the text and display it on the screen
        text = self.font.render(velocity_text, True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 150, 30))
        text = self.font.render(terminal_velocity_text, True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 150, 50))
    
    def _draw_wind_info(self):
        # Screen center for arrow placement
        arrow_start = Vector2(SCREEN_WIDTH - 150, 80)
        wind_magnitude = self.wind.length()  # Magnitude of the wind
        wind_direction = self.wind.normalize() if wind_magnitude > 0 else Vector2(0, 0)

        # Arrow end point
        arrow_end = arrow_start + wind_direction * 50  # Scale arrow length

        # Draw the arrow (line)
        pygame.draw.line(self.screen, (0, 0, 255), arrow_start, arrow_end, 3)

        # Draw arrowhead
        angle = math.atan2(wind_direction.y, wind_direction.x)
        arrowhead_length = 10
        left_arrowhead = arrow_end + Vector2(-math.cos(angle + math.pi / 6), -math.sin(angle + math.pi / 6)) * arrowhead_length
        right_arrowhead = arrow_end + Vector2(-math.cos(angle - math.pi / 6), -math.sin(angle - math.pi / 6)) * arrowhead_length
        pygame.draw.line(self.screen, (0, 0, 255), arrow_end, left_arrowhead, 2)
        pygame.draw.line(self.screen, (0, 0, 255), arrow_end, right_arrowhead, 2)

        # Display the wind magnitude as text
        wind_text = f"Wind: {wind_magnitude:.2f} m/s"
        text = self.font.render(wind_text, True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 150, 90))

    def _draw_info(self):
        self._draw_scale()
        self._draw_time_counter()
        self._draw_grenade_velocity()
        self._draw_wind_info()