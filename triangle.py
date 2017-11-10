import math

EPS = 0


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def to_lines(self):
        return [
            (self.a, self.b),
            (self.b, self.c),
            # [self.c, self.a]
        ]

    def transform(self, options):
        points = [self.a, self.b, self.c]
        points = [point.transform(options) for point in points]
        return Triangle(points[0], points[1], points[2])

    def is_point_inside(self, point):
        x = point.x
        y = point.y

        x1 = self.a.x
        y1 = self.a.y
        x2 = self.b.x
        y2 = self.b.y
        x3 = self.c.x
        y3 = self.c.y

        if (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1) == 0 or x2 - x1 == 0:
            return True

        m3 = ((x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)) / ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1))
        m2 = (x - x1 - m3 * (x3 - x1)) / (x2 - x1)
        m1 = round(1 - m2 - m3, 2)

        return m3 >= EPS and m2 >= EPS and m1 >= EPS

    def get_z_index(self):
        return min(self.a.z, self.b.z, self.c.z)
