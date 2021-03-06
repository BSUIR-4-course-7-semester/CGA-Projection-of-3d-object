import math

import numpy
from sdl2 import SDL_Point

Rx = lambda th: [
    [1, 0, 0, 0],
    [0, math.cos(th), math.sin(th), 0],
    [0, -math.sin(th), math.cos(th), 0],
    [0, 0, 0, 1]
]

Rz = lambda th: [
    [math.cos(th), -math.sin(th), 0, 0],
    [math.sin(th), math.cos(th), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

Ry = lambda th: [
    [math.cos(th), 0, math.sin(th), 0],
    [0, 1, 0, 0],
    [-math.sin(th), 0, math.cos(th), 0],
    [0, 0, 0, 1]
]

T = lambda d: [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [d[0], d[1], d[2], 1]
]

S = lambda s: [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1/s]
]


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, value):
        return Point3D(self.x + value.x, self.y + value.y, self.z + value.z)

    def __repr__(self):
        return 'x={0}, y={1}, z={2}'.format(self.x, self.y, self.z)

    def to_uniform_coordinates(self):
        return [self.x, self.y, self.z, 1]

    @staticmethod
    def from_uniform_coordinates(point):
        return Point3D(
            int(point[0] / point[3]),
            int(point[1] / point[3]),
            int(point[2] / point[3])
        )

    @staticmethod
    def rotate_x(point, angle):
        return numpy.dot(Rx(angle), point)

    @staticmethod
    def rotate_z(point, angle):
        return numpy.dot(Rz(angle), point)

    @staticmethod
    def rotate_y(point, angle):
        return numpy.dot(Ry(angle), point)

    @staticmethod
    def translate(point, dx, dy, dz):
        return numpy.dot(T([dx, dy, dz]), point)

    @staticmethod
    def scale(point, s):
        return numpy.dot(S(s), point)

    @staticmethod
    def apply_camera(point, camera_matrix):
        res = numpy.dot(camera_matrix, point)
        return res

    def transform(self, options, camera):
        uniform_point = self.to_uniform_coordinates()

        final_matrix = self.get_transforming_matrix(options, camera)

        uniform_point = numpy.dot(uniform_point, final_matrix)

        p = Point3D.from_uniform_coordinates(uniform_point)

        return p

    @staticmethod
    def get_transforming_matrix(options, camera):
        # return numpy.dot(
        #     numpy.dot(
        #         Rx(options.x_angle),
        #         numpy.dot(
        #             Ry(options.y_angle),
        #             numpy.dot(
        #                 Rz(options.z_angle),
        #                 numpy.dot(
        #                     S(options.scale),
        #                     T([options.dx, options.dy, options.dz])
        #                 )
        #             )
        #         )
        #     ),
        #     camera.get_projection_matrix()
        # )

        return numpy.dot(
            S(options.scale),
            numpy.dot(
                T([options.dx, options.dy, options.dz]),
                numpy.dot(
                    Rx(options.x_angle),
                    numpy.dot(
                        Ry(options.y_angle),
                        numpy.dot(
                            Rz(options.z_angle),
                            camera.get_projection_matrix()
                        )
                    )
                )
            )
        )

    def __eq__(self, p):
        return p.x == self.x and p.y == self.y and p.z == self.z
