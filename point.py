from sdl2 import SDL_Point


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, value):
        return Point3D(self.x + value.x, self.y + value.y, self.z + value.z)

    def __repr__(self):
        return 'x={0}, y={1}, z={2}'.format(self.x, self.y, self.z)
