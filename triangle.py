import math
import numpy as np

from edge import Edge

# EPS = 0.035
EPS = 0.0


def calc_barycentric(triangle, point):
    barycentric = None

    u = np.cross(
        [triangle.c.x - triangle.a.x, triangle.b.x - triangle.a.x, triangle.a.x - point.x],
        [triangle.c.y - triangle.a.y, triangle.b.y - triangle.a.y, triangle.a.y - point.y]
    )

    if abs(u[2]) < 1:
        barycentric = [-1, 1, 1]
    else:
        barycentric = [
            1 - (u[0] + u[1]) / u[2],
            u[1] / u[2],
            u[0] / u[2]
        ]

    return barycentric


def has_line(lines, line):
    for l in lines:
        if l == line:
            return True

    return False


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def to_lines(self):
        return [
            Edge(self.a, self.b),
            Edge(self.b, self.c),
            # [self.c, self.a]
        ]

    def transform(self, options, camera):
        points = [self.a, self.b, self.c]
        points = [point.transform(options, camera) for point in points]
        return Triangle(points[0], points[1], points[2])

    def is_point_inside(self, point):
        barycentric = calc_barycentric(self, point)

        result = barycentric[2] >= EPS and barycentric[1] >= EPS and barycentric[0] >= EPS

        return result, barycentric

    def get_z_index(self, barycentric_coords_of_point):
        return sum([
            self.a.z * barycentric_coords_of_point[0],
            self.b.z * barycentric_coords_of_point[1],
            self.c.z * barycentric_coords_of_point[2]
        ]) + 7  # it's because of error in calculating of z coordinate on triangle by barycentric

    def has_line(self, line):
        return has_line(self.to_lines(), line)
