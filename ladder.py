import math

from point import Point3D
from transform_options import TransformOptions
from triangle import Triangle


class Ladder:
    def __init__(self, step_height, width, step_count):
        if step_count < 1:
            raise Exception('Step count must be more than 0')

        self.triangles = []
        self.x_angle = 0.85
        self.y_angle = 1.57
        self.z_angle = 0
        self.dx = 275
        self.dy = 125
        self.dz = 0
        self.scale = 0.2

        self._step_height = step_height
        self._step_length = step_height * 2
        self._width = width
        self._step_count = step_count
        self._base_point = Point3D()

        self._generate()

    def _generate(self):
        self._generate_base()
        self._generate_back()

        for step_number in range(self._step_count):
            self._generate_step(step_number)

    def _generate_step(self, step_number):
        a = self._l_b + Point3D(y=-(step_number * self._step_length))
        b = a + Point3D(z=self._step_height * (step_number + 1))
        c = b + Point3D(y=-self._step_length)
        d = a + Point3D(y=-self._step_length)
        f = b + Point3D(z=-self._step_height)
        a1 = a + Point3D(x=self._width)
        b1 = b + Point3D(x=self._width)
        c1 = c + Point3D(x=self._width)
        d1 = d + Point3D(x=self._width)
        f1 = f + Point3D(x=self._width)

        self.triangles.append(Triangle(a, b, c))
        self.triangles.append(Triangle(a, d, c))

        self.triangles.append(Triangle(a1, b1, c1))
        self.triangles.append(Triangle(a1, d1, c1))

        self.triangles.append(Triangle(b, f, f1))
        self.triangles.append(Triangle(f1, b1, b))

        self.triangles.append(Triangle(c, b, b1))
        self.triangles.append(Triangle(b1, c1, c))

    def _generate_back(self):
        a = self._l_t + Point3D(z=self._step_count * self._step_height)
        b = a + Point3D(self._width)

        self.triangles.append(Triangle(a, b, self._r_t))
        self.triangles.append(Triangle(a, self._l_t, self._r_t))

    def _generate_base(self):
        self._l_t = self._base_point
        self._r_t = self._l_t + Point3D(self._width)
        self._r_b = self._r_t + Point3D(y=self._step_count * self._step_length)
        self._l_b = self._r_b + Point3D(x=-self._width)

        self.triangles.append(Triangle(self._l_t, self._r_t, self._r_b))
        self.triangles.append(Triangle(self._l_t, self._l_b, self._r_b))

    def rotate_x(self, d_angle):
        self.x_angle += math.radians(d_angle)

    def rotate_y(self, d_angle):
        self.y_angle += math.radians(d_angle)

    def rotate_z(self, d_angle):
        self.z_angle += math.radians(d_angle)

    def translate_x(self, d):
        self.dx += d

    def translate_y(self, d):
        self.dy += d

    def translate_z(self, d):
        self.dz += d

    def plus_scale(self):
        self.scale += 0.1

    def minus_scale(self):
        self.scale -= 0.1

    def get_transform_options(self):
        return TransformOptions(
            self.x_angle,
            self.y_angle,
            self.z_angle,
            self.scale,
            self.dx,
            self.dy,
            self.dz
        )



