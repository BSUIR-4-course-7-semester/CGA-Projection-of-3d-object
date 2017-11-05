from point import Point3D
from triangle import Triangle


class Ladder:
    def __init__(self, step_height, width, step_count):
        if step_count < 1:
            raise Exception('Step count must be more than 0')

        self.triangles = []

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

        self.triangles.append(Triangle(f, f1, b))
        self.triangles.append(Triangle(b, b1, f1))

        self.triangles.append(Triangle(b, c, b1))
        self.triangles.append(Triangle(c1, b1, c))

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




