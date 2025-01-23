import random
import math

import pygame
from pygame.math import Vector2

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS, PIXELS_PER_METER, WIDTH, HEIGHT
from entities import Grenade, Drone, Enemy


class Environment:
    def __init__(self, mode="human"):
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
        self._initialize_entities()
        self.score = 0  # Initialize score
        self.current_action = None
        self.mode = mode  # "human" or "rl"
        self.action_space = [0, 1, 2]

    def reset(self):
        self.time_elapsed = 0
        self.wind = self._generate_wind()
        self._initialize_entities()
        self.score = 0
        return self.get_state()

    def get_state(self):
        # Represent the state as a vector
        return [
            self.drone.position.x, self.drone.position.y,
            self.grenade.position.x, self.grenade.position.y,
            self.enemy.position.x,
            self.wind.x, self.wind.y
        ]

    def step(self, action, render=True):
        self.current_action = None
        if action == 0:
            self.current_action = "drone_left"
        elif action == 1:
            self.current_action = "drone_right"
        elif action == 2:
            self.current_action = "drone_release"

        # Update the environment
        self.update()

        # Render the environment if requested
        if render:
            self.render()
            pygame.display.flip()  # Update the display

        # Check if the episode is done
        done = self.grenade.hit_ground

        # Get the reward
        reward = self._calculate_score() if done else 0

        # Get the next state
        state = self.get_state()

        return state, reward, done, {}

    def update(self):
        dt = self.clock.tick(FPS) / 1000.0
        self.time_elapsed += dt
        self.drone.update(dt, self.current_action)
        self.grenade.update(dt, self.wind)
        self.enemy.update()
        if self.grenade.hit_ground:
            self.score = self._calculate_score()

    def render(self):
        """Render all elements to the screen."""
        # Fill the screen with the background color
        self.screen.fill(self.background_color)
        self._draw_info()
        self.drone.render(self.screen)
        self.grenade.render(self.screen)
        self.enemy.render(self.screen)

    def run(self):
        running = True
        while running:
            # Handle events for human control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_action = "drone_left"
                    elif event.key == pygame.K_RIGHT:
                        self.current_action = "drone_right"
                    elif event.key == pygame.K_SPACE:
                        self.current_action = "drone_release"
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE):
                        self.current_action = None

            # Update and render the environment
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def _generate_wind(self):
        wind_speed = pygame.math.Vector2(random.uniform(-35, 35), 0)
        return wind_speed

    def _initialize_entities(self):
        self.drone = Drone(random.randint(40, WIDTH-40), random.randint(0, HEIGHT-90))
        self.grenade = self.drone.grenade
        self.enemy = Enemy(random.randint(20, WIDTH-20))

    def _calculate_score(self):
        # Calculate distance to enemy (enemy is a square at the bottom)
        enemy_position = self.enemy.position
        grenade_position = self.grenade.position
        # Calculate the horizontal (X) distance between the grenade and the enemy
        x_distance = abs(grenade_position.x - enemy_position.x)
        
        # Check if the grenade is within 5 meters horizontally of the enemy
        if x_distance <= 10:  # 5 meters range
            # Calculate the reward based on the distance (this is just an example)
            reward = max(0, 100 - int(x_distance * 20))  # Decreases with distance, max reward = 100
            return reward  # Return the calculated reward
        else:
            return 0  # No reward if outside the range

    def _draw_scale(self):
        for y in range(0, HEIGHT+20, 20):
            text = self.font.render(f"{y} meters", True, (0, 0, 0))
            self.screen.blit(text, (5, SCREEN_HEIGHT-(y*5)))

    def _draw_time_counter(self):
        time_text = f"Time: {self.time_elapsed:.2f} s"
        text = self.font.render(time_text, True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 150, 10))

    def _draw_grenade_velocity(self):
        # Get the magnitude (speed) of the velocity vector
        velocity_magnitude = self.grenade.velocity.length()  # This gives the speed as a scalar value (m/s)
        # Create the text to display the current velocity and terminal velocity
        velocity_text = f"Velocity: {velocity_magnitude:.2f} m/s"
        terminal_velocity_text = f"T.Velocity: {self.grenade.terminal_velocity:.2f} m/s"        
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

    def _draw_score(self):
        # Display score
        score_text = f"Score: {self.score}"
        text = self.font.render(score_text, True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 150, 110))
    
    def _draw_info(self):
        self._draw_scale()
        self._draw_time_counter()
        self._draw_grenade_velocity()
        self._draw_wind_info()
        self._draw_score()
