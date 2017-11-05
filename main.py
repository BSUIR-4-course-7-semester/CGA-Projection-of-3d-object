import sdl2.ext
import sys

from sdl2 import SDL_Point
from sdl2.examples.pixelaccess import WHITE

from drawing import draw_line
from ladder import Ladder


def adapt_3d_point_to_front_projection(point3d):
    return SDL_Point(point3d.x, point3d.z)


def adapt_3d_point_to_right_projection(point3d):
    return SDL_Point(point3d.y, point3d.z)


def adapt_3d_point_to_up_projection(point3d):
    return SDL_Point(point3d.x, point3d.y)


def draw_projection(pixels, figures, adapt_point_func):
    lines = []
    for figure in figures:
        for triangle in figure.triangles:
            lines += triangle.to_lines()

    lines = [
        [
            adapt_point_func(line[0]),
            adapt_point_func(line[1])
        ] for line in lines]

    for line in lines:
        draw_line(pixels, line[0], line[1], WHITE)


def main():

    sdl2.ext.init()
    window = sdl2.ext.Window("Filled polygon", size=(640, 480))
    window.show()

    window_surface = window.get_surface()
    pixels = sdl2.ext.PixelView(window_surface)

    running = True

    ladder = Ladder(20, 50, 10)

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

        draw_projection(pixels, [ladder], adapt_3d_point_to_front_projection)

        window.refresh()

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())