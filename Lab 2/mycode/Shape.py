import math

class Shape:
    class BadSidesException(Exception):
        def __str__(self):
            return "Shape cannot be instantiated with less than 3 sides"

    def __init__(self, sides, radius, center=(0, 0), color="#FFFFFF"):
        self.sides = sides
        self.radius = radius
        self.center = center
        self.phase = 0
        self.color = color

    def translate(self, translate_vector):
        centerX, centerY = self.center
        dX, dY = translate_vector

        self.center = (centerX + dX, centerY + dY)

    def transform(self, factor):
        self.radius *= factor

    # RADIANS
    def rotate(self, radians):
        self.phase += radians

    def get_points(self):
        points = []
        rad = 0
        centerX, centerY = self.center

        while rad < 2 * math.pi:
            point_x = self.radius * math.cos(rad + self.phase) + centerX
            point_y = self.radius * math.sin(rad + self.phase) + centerY

            points.append((point_x, point_y))

            rad += 2 * math.pi / self.sides

        return points

    def render_shape(self, draw):
        points = self.get_points()
        draw.polygon(points, fill=self.color, outline="#FFFFFF")



class TwoSidedShape(Shape):
    def __init__(self, radius, center=(0, 0), color="#FFFFFF"):
        self.radius = radius
        self.center = center
        self.phase = 0
        self.color = color

    def get_points(self):
        points = []
        rad = 0
        centerX, centerY = self.center

        while rad < 2 * math.pi:
            point_x = self.radius * math.cos(rad + self.phase) + centerX
            point_y = self.radius * math.sin(rad + self.phase) + centerY

            points.append((point_x, point_y))

            rad += 2 * math.pi / 3

        return points

    def render_shape(self, draw):
        points = self.get_points()
        draw.line((points[0][0], points[0][1], points[1][0], points[1][1]), fill="#FFFFFF")
        draw.line((points[2][0], points[2][1], points[1][0], points[1][1]), fill="#FFFFFF")

def create_shape(sides, radius, center=(0, 0), color = "#FFFFFF"):
    if sides == 2:
        return TwoSidedShape(radius, center)

    if sides == 1:
        return Shape(2, radius, center, color)

    if sides == 0:
        return Shape(100, radius, center, color)
    
    return Shape(sides, radius, center, color)

if __name__ == '__main__':
    s = Shape(4, 10)
    print(s.get_points())

    s.transform(0.5)
    print(s.get_points())
