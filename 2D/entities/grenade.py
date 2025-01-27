import math

import pygame

from utils import Vector
from constants import PIXELS_PER_METER, HEIGHT, GRAVITY, AIR_DENSITY

class Grenade:
    def __init__(self, x, y, radius=0.032, mass=0.4, drag_coefficient=0.47):
        """
        Initializes the grenade with basic properties such as position, velocity, and physical characteristics.
        
        Args:
            x (float): The initial x-coordinate of the grenade.
            y (float): The initial y-coordinate of the grenade.
            radius (float): The radius of the grenade in meters (default: 0.032 m).
            mass (float): The mass of the grenade in kilograms (default: 0.4 kg).
            drag_coefficient (float): The drag coefficient for the grenade (default: 0.47).
        """
        self.coordinates = Vector(x, y)
        self.velocity = Vector(0, 0)

        self.radius = radius  # m (radius in meters)
        self.mass = mass  # kg (mass in kilograms)
        self.drag_coefficient = drag_coefficient  # Drag coefficient for a sphere
        self.cross_sectional_area = math.pi * (self.radius ** 2)  # m^2
        self.terminal_velocity = self._calculate_terminal_velocity()  # m/s

        self.released = False  # Flag to track if grenade is released
        self.hit_ground = False  # Flag to track if grenade has hit the ground

    def update(self, wind, dt, max_altitude=HEIGHT):
        """
        Updates the grenade's position based on forces (gravity, wind) and velocity.

        Args:
            wind (Vector): The wind vector affecting the grenade's motion.
            dt (float): The time step for the simulation.
            max_altitude (float): The maximum altitude (in meters) to scale wind forces (default: HEIGHT).
        """
        if self.released and not self.hit_ground:
            # Calculate gravitational force
            gravitational_force = self._calculate_gravity_force()
            # Calculate relative velocity: wind is moving, so we subtract it from the grenade's velocity
            relative_velocity = self.velocity - wind
            # Calculate drag force based on relative velocity (quadratic drag equation)
            if relative_velocity.magnitude() > 0:
                drag_force = (
                    relative_velocity.normalize() * -0.5 * AIR_DENSITY * self.drag_coefficient * self.cross_sectional_area *
                    relative_velocity.magnitude_squared()
                )
            else:
                drag_force = Vector(0, 0)  # No drag if relative velocity is zero (e.g., initially stationary)
            # The total net force is the sum of gravity and drag forces
            net_force = gravitational_force + drag_force
            # Calculate acceleration from net force (F = ma)
            acceleration = net_force / self.mass
            # Update velocity by integrating acceleration over time
            self.velocity += acceleration * dt
            # Cap the velocity at terminal velocity to prevent infinite speed
            if self.velocity.magnitude() > self.terminal_velocity:
                self.velocity = self.velocity.normalize() * self.terminal_velocity
            # Update the position using the updated velocity
            self.coordinates += self.velocity * dt
            # Check for collision with the ground
            if self.coordinates.y >= HEIGHT:
                self.coordinates.y = HEIGHT  # Ensure the grenade doesn't fall below the ground level
                self.velocity.y = 0  # Stop vertical velocity
                self.hit_ground = True  # Mark as hit ground

    def _calculate_gravity_force(self):
        """Calculates the gravitational force acting on the grenade."""
        return Vector(0, self.mass * GRAVITY)
    
    def _calculate_wind_force_at_attitude(self, wind, max_altitude):
        """
        Calculates the wind force on the grenade based on its current altitude.
        
        Args:
            wind (Vector): The wind vector at sea level (in meters per second).
            max_altitude (float): The maximum altitude (in meters) for wind scaling.

        Returns:
            Vector: The adjusted wind force based on the grenade's altitude.
        """
        altitude = max_altitude - self.coordinates.y  # Altitude above ground
        altitude_factor = max(min(altitude / max_altitude, 1.0), 0.0)  # Normalize the altitude factor
        return wind * altitude_factor

    def _calculate_terminal_velocity(self):
        """
        Calculates the terminal velocity for the grenade using the drag equation.
        
        Returns:
            float: The terminal velocity of the grenade in meters per second.
        """
        return math.sqrt(
            (2 * self.mass * GRAVITY) / (AIR_DENSITY * self.drag_coefficient * self.cross_sectional_area)
        )
    
    def render(self, screen, pixels_per_meter):
        # Convert position to pixels for rendering
        position_pixels = self.coordinates * pixels_per_meter
        pygame.draw.circle(
            screen, (200, 50, 50), 
            (int(position_pixels.x), int(position_pixels.y)), 
            5
        )