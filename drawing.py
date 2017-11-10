from sdl2 import SDL_Point
from sdl2.examples.pixelaccess import BLACK

from point import Point3D


def get_pixel(pixels, point):
    return pixels[point.y][point.x]


def put_pixel(pixels, point, color):
    if point.x < 0 or point.x >= 640 or point.y < 0 or point.y >= 480:
        return
    pixels[point.y][point.x] = color


def is_hidden(point, z_index, triangles):
    result = False

    for triangle in triangles:
        if triangle.is_point_inside(point) and triangle.get_z_index() > z_index:
            result = True
            break

    return result


def draw_line(pixels, line, visible_color, hidden_color, triangles):
    hidden_color = BLACK

    steep = False

    is_last_hidden = False

    x0 = line[0].x
    y0 = line[0].y
    x1 = line[1].x
    y1 = line[1].y
    z0 = line[0].z
    z1 = line[1].z

    z_index = (z0 + z1) / 2

    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0

    if dx == 0:
        return

    dy = (y1 - y0) / dx

    y = y0

    for x in range(x0, x1 + 1):
        point_to_draw = None

        if steep:
            point_to_draw = SDL_Point(int(y), x)
        else:
            point_to_draw = SDL_Point(x, int(y))

        is_current_hidden = is_hidden(point_to_draw, z_index, triangles)

        put_pixel(pixels, point_to_draw, hidden_color if is_current_hidden else visible_color)

        y += dy
