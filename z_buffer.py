import numpy
from sdl2 import SDL_Point
from sdl2.examples.gui import GREEN
from sdl2.examples.pixelaccess import BLACK


class ZBufferItem:
    def __init__(self, z_index, color, is_border, is_hidden=False):
        self.z_index = z_index
        self.color = color
        self.is_border = is_border


class ZBuffer:
    def __init__(self, width, height):
        self.surface = [[None for j in range(480)] for i in range(640)]

    def put_pixel(self, x, y, color, z_index, is_border=False):
        item = self.surface[x][y]

        if item is None or item.z_index < z_index:

            self.surface[x][y] = ZBufferItem(z_index, color, is_border)

    def get_color(self, x, y):
        item = self.surface[x][y]

        if item is not None:
            return GREEN
        else:
            return BLACK

        if item.is_border:
            if item.is_hidden:
                return BLACK
            else:
                return GREEN

        return None

    def rasterize_triangle(self, triangle):
        x0 = triangle.a.x
        y0 = triangle.a.y

        x1 = triangle.b.x
        y1 = triangle.b.y

        x2 = triangle.c.x
        y2 = triangle.c.y

        left_x = min(x0, x1, x2)
        right_x = max(x0, x1, x2)

        top_y = min(y0, y1, y2)
        bottom_y = max(y0, y1, y2)

        for i in range(left_x, right_x + 1):
            for j in range(top_y, bottom_y + 1):
                if triangle.is_point_inside(SDL_Point(i, j)):
                    self.put_pixel(i, j, None, max(triangle.a.z, triangle.b.z, triangle.c.z), False)

    def draw_line(self, line):
        pass
