import random
import time
import math

import pygame

from constants import WIDTH, HEIGHT, WIND_FORCE_MAX, PIXELS_PER_METER, RENDER_PAUSE
from utils import Vector
from entities import Drone, Grenade, Target

class Environment:
    def __init__(self, dt=0.1, max_steps=100, drone_min_height = 0.5, renderMode=False):
        self.dt = dt
        self.max_steps=max_steps
        self.drone_min_height = drone_min_height
        self.width = WIDTH
        self.height = HEIGHT

        self.renderMode = renderMode
        self.screen = None

    def reset(self):
        self.drone = Drone(random.randint(0, WIDTH), random.randint(0, HEIGHT-(HEIGHT*self.drone_min_height)))
        self.grenade = self.drone.attach_grenade()
        self.target = Target(random.randint(40, WIDTH-40))
        self.wind = self.generateWindForce()
        self.steps = 0
        self.score = 0

        if self.renderMode and self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width*PIXELS_PER_METER, self.height*PIXELS_PER_METER))
            self.font = pygame.font.SysFont(None, 20)

        return self._get_observation()

    def step(self, action):
        self.drone.update(action, self.dt)
        self.grenade.update(self.wind, self.dt)
        self.steps += 1

        done = self._is_done()
        reward = self._calculate_reward()
        observation = self._get_observation()

        return observation, reward, done, {}

    def _get_observation(self):
        observation = [
            self.drone.coordinates.x, self.drone.coordinates.y,
            self.grenade.coordinates.x, self.grenade.coordinates.y,
            self.target.coordinates.x, self.target.coordinates.y,
            self.wind.x, self.wind.y,
            int(self.grenade.released)
        ]
        return observation

    def _calculate_reward(self):
        if self.grenade.hit_ground:
            target_coordinates = self.target.coordinates
            grenade_coordinates = self.grenade.coordinates
            # Calculate the horizontal (X) distance between the grenade and the target
            distance = abs((target_coordinates - grenade_coordinates).magnitude())

            if distance < 0:
                # Pinpoint hit: perfect landing on the target
                reward = 1000
            elif distance <= 10:
                # Within range of 10 meters: decaying reward
                reward = max(0, 100 - distance*10) # Decaying reward as the distance increases
            else:
                # Outside range of 10 meters: decaying penalty
                penalty = min(0, distance * 10)  # Increasing penalty as the distance grows
                reward = -penalty  # Negative penalty for missing the target area

            return reward
        return -1


    def _is_done(self):
        return self.grenade.hit_ground

    def generateWindForce(self):
        return Vector(random.uniform(-WIND_FORCE_MAX, WIND_FORCE_MAX), 0)

    def render(self):
        if not self.renderMode:
            raise Exception("Render is not True.")
        if self.screen is None:
            raise Exception("Pygame not initialized. Call reset() or set renderMode=True before rendering.")

        self.screen.fill((180, 180, 180))  # Clear the screen

        # Draw objects (dummy example)
        self.drone.render(self.screen, PIXELS_PER_METER)
        self.grenade.render(self.screen, PIXELS_PER_METER)
        self.target.render(self.screen, PIXELS_PER_METER)

        self._draw_info()

        pygame.display.flip()
        
        time.sleep(RENDER_PAUSE)

    def close(self):
        if self.renderMode:
            pygame.quit()

    def _draw_scale(self):
        for y in range(0, HEIGHT, 20):
            text = self.font.render(f"{y} meters", True, (0, 0, 0))
            self.screen.blit(text, (5, (HEIGHT - y) * PIXELS_PER_METER))

    def _draw_time_counter(self):
        total_time = self.steps * self.dt  # Total simulation time
        minutes = int(total_time // 60)  # Integer division to get seconds
        seconds = total_time % 60  # Get the remainder for microseconds
        rounded_seconds = round(seconds, 2)  # Round to two decimal places for seconds

        time_text = f"Time: {minutes:02}:{rounded_seconds:05.2f}"  # Format as mm:ss.xx
        text = self.font.render(time_text, True, (0, 0, 0))
        self.screen.blit(text, (WIDTH * PIXELS_PER_METER - 150, 10))

    def _draw_grenade_velocity(self):
        velocity_magnitude = self.grenade.velocity.magnitude()
        terminal_velocity_text = f"T.Velocity: {self.grenade.terminal_velocity:.2f} m/s"
        velocity_text = f"Velocity: {velocity_magnitude:.2f} m/s"

        text = self.font.render(velocity_text, True, (0, 0, 0))
        self.screen.blit(text, (WIDTH * PIXELS_PER_METER - 150, 30))
        text = self.font.render(terminal_velocity_text, True, (0, 0, 0))
        self.screen.blit(text, (WIDTH * PIXELS_PER_METER - 150, 50))

    def _draw_wind_info(self):
        wind_magnitude = self.wind.x
        wind_text = f"Wind: {wind_magnitude:.2f} m/s"
        text = self.font.render(wind_text, True, (0, 0, 0))
        self.screen.blit(text, (WIDTH * PIXELS_PER_METER - 150, 90))

    def _draw_score(self):
        score_text = f"Score: {self.score}"
        text = self.font.render(score_text, True, (0, 0, 0))
        self.screen.blit(text, (WIDTH * PIXELS_PER_METER - 150, 110))

    def _draw_info(self):
        self._draw_scale()
        self._draw_time_counter()
        self._draw_grenade_velocity()
        self._draw_wind_info()
        self._draw_score()