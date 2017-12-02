import math
from sdl2 import SDL_Point


def get_pixel(pixels, point):
    return pixels[point.y][point.x]


def put_pixel(pixels, point, color):
    # axis shifting
    x = point.x + 200
    y = point.y + 100

    if x < 0 or x >= 640 or y < 0 or y >= 480:
        return
    pixels[y][x] = color


def is_hidden(point, z_index, triangles, line):
    result = False

    for triangle in triangles:
        if triangle.has_line(line):
            continue

        is_inside, barycentric_coords = triangle.is_point_inside(point)

        if is_inside:
            z_on_triangle = triangle.get_z_index(barycentric_coords)
            if z_on_triangle < z_index:
                result = True
                break

    return result


def draw_line(pixels, line, visible_color, hidden_color, triangles):
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
        z0, z1 = z1, z0

    dx = x1 - x0

    if dx == 0:
        return

    dy = (y1 - y0) / dx
    dz = (z1 - z0) / dx

    y = y0
    z = z0

    divider = 10

    for x in range(x0, x1 + 1):
        point_to_draw = None

        if steep:
            point_to_draw = SDL_Point(int(y), x)
        else:
            point_to_draw = SDL_Point(x, int(y))

        is_current_hidden = is_hidden(point_to_draw, z, triangles, line)

        color = None if is_current_hidden and (dash != 0 and dash < divider / 2) else visible_color

        if color is not None:
            put_pixel(pixels, point_to_draw, color)

        y += dy
        z += dz

        dash = (dash + 1) % divider if is_current_hidden else 0
