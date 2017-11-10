from sdl2 import SDL_Point
from sdl2.examples.gui import GREEN
from sdl2.examples.pixelaccess import BLACK, WHITE

from point import Point3D

WHITE_INT = 16777215
GREEN_INT = 65280

def get_pixel(pixels, point):
    return pixels[point.y][point.x]


def put_pixel(pixels, point, color):
    if point.x < 0 or point.x >= 640 or point.y < 0 or point.y >= 480:
        return
    pixels[point.y][point.x] = color


def is_hidden(point, z_index, triangles, line):
    result = False

    for triangle in triangles:
        if not triangle.has_line(line) and triangle.is_point_inside(point) and triangle.get_z_index() > z_index:
            result = True
            break

    return result


def draw_line(pixels, line, visible_color, hidden_color, triangles):
    # hidden_color = BLACK

    steep = False

    dash = 0

    x0 = line[0].x
    y0 = line[0].y
    x1 = line[1].x
    y1 = line[1].y
    z0 = line[0].z
    z1 = line[1].z

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
    dz = (z1 - z0) / dx

    y = y0
    z = z0

    for x in range(x0, x1 + 1):
        point_to_draw = None

        if steep:
            point_to_draw = SDL_Point(int(y), x)
        else:
            point_to_draw = SDL_Point(x, int(y))

        is_current_hidden = is_hidden(point_to_draw, z, triangles, line)

        pixel = get_pixel(pixels, point_to_draw)

        color = BLACK if is_current_hidden and dash == 1 else visible_color

        if color == GREEN or pixel != GREEN_INT:
            put_pixel(pixels, point_to_draw, color)

        y += dy
        z += dz

        dash = (dash + 1) % 2 if is_current_hidden else 0
