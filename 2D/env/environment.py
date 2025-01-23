import pygame

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

        self.entities = self._initialize_entities()

    def update(self):
        dt = self.clock.tick(FPS) / 1000.0
        self.time_elapsed += dt
        for entity in self.entities:
            entity.update(dt)

    def render(self):
        """Render all elements to the screen."""
        # Fill the screen with the background color
        self.screen.fill(self.background_color)
        # Draw the scale
        self._draw_scale()
        # Display time elapsed
        self._draw_time_counter()
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
