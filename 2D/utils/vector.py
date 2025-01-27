import math

class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector(self.x / scalar, self.y / scalar)
        raise ValueError("Cannot divide by zero.")

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def magnitude_squared(self):
        return self.magnitude()**2

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            x = self.x / mag
            y = self.y / mag
            return Vector(x, y)
        else:
            raise ValueError("Cannot normalize a zero vector.")

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x