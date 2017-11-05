from sdl2 import SDL_Point


def get_pixel(pixels, point):
    return pixels[point.y][point.x]


def put_pixel(pixels, point, color):
    pixels[point.y][point.x] = color


def draw_line(pixels, point_a, point_b, color):
    dx = abs(point_a.x - point_b.x)
    dy = abs(point_a.y - point_b.y)

    sx = 1 if point_b.x >= point_a.x else -1
    sy = 1 if point_b.y >= point_a.y else -1

    if dy <= dx:
        d = dy * 2 - dx
        d1 = dy * 2
        d2 = (dy - dx) * 2

        put_pixel(pixels, point_a, color)
        x = point_a.x + sx
        y = point_a.y
        for i in range(1, dx + 1):
            if d > 0:
                d += d2
                y += sy
            else:
                d += d1

            put_pixel(pixels, SDL_Point(x, y), color)
            x += sx
    else:
        d = dx * 2 - dy
        d1 = dx * 2
        d2 = (dx - dy) * 2

        put_pixel(pixels, point_a, color)
        x = point_a.x
        y = point_a.y + sy
        for i in range(1, dy + 1):
            if d > 0:
                d += d2
                x += sx
            else:
                d += d1

            put_pixel(pixels, SDL_Point(x, y), color)
            y += sy
