import numpy
import sdl2.ext
import sys

from sdl2 import SDL_Point, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_z, SDLK_x, SDLK_y, SDLK_t, SDLK_s, SDLK_r
from sdl2.examples.pixelaccess import WHITE, BLACK

from camera import Camera
from drawing import draw_line
from ladder import Ladder
from point import Point3D

T = 't'
R = 'r'
S = 's'

X = 'x'
Y = 'y'
Z = 'z'


def adapt_3d_point_to_front_projection(point3d):
    # return SDL_Point(point3d.x, point3d.z)
    res = Point3D.from_uniform_coordinates(numpy.dot([
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], point3d.to_uniform_coordinates()))
    return SDL_Point(res.x, res.z)


def adapt_3d_point_to_projection(point3d, camera):
    res = Point3D.from_uniform_coordinates(
        numpy.dot(camera.projection_matrix, point3d.to_uniform_coordinates())
    )
    return SDL_Point(res.x, res.z)

def adapt_3d_point_to_right_projection(point3d):
    return SDL_Point(point3d.y, point3d.z)


def adapt_3d_point_to_up_projection(point3d):
    return SDL_Point(point3d.x, point3d.y)


def draw_projection(pixels, camera, figures, adapt_point_func):
    lines = []
    for figure in figures:
        transform_options = figure.get_transform_options()

        for triangle in figure.triangles:
            lines += triangle.transform(transform_options).to_lines()

    lines = [
        [
            adapt_point_func(line[0]),
            adapt_point_func(line[1])
        ] for line in lines]

    for line in lines:
        draw_line(pixels, line[0], line[1], WHITE)


def clear(surface):
    sdl2.ext.fill(surface, BLACK)


def main():

    sdl2.ext.init()
    window = sdl2.ext.Window("3d", size=(640, 480))
    window.show()

    window_surface = window.get_surface()
    pixels = sdl2.ext.PixelView(window_surface)

    running = True

    camera = Camera(640, 480, 20, 300)
    ladder = Ladder(20, 50, 2)

    operation = R
    selected_axis = Z

    is_changed = True

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_z:
                    print('selected Z')
                    selected_axis = Z
                elif event.key.keysym.sym == SDLK_x:
                    print('selected X')
                    selected_axis = X
                elif event.key.keysym.sym == SDLK_y:
                    print('selected Y')
                    selected_axis = Y

                elif event.key.keysym.sym == SDLK_t:
                    print('selected translating')
                    operation = T
                elif event.key.keysym.sym == SDLK_s:
                    print('selected scaling')
                    operation = S
                elif event.key.keysym.sym == SDLK_r:
                    print('selected rotating')
                    operation = R

                elif event.key.keysym.sym == SDLK_RIGHT or event.key.keysym.sym == SDLK_LEFT:
                    sign = 1 if event.key.keysym.sym == SDLK_RIGHT else -1
                    is_changed = True
                    if operation == T:
                        if selected_axis == X:
                            ladder.translate_x(sign * 5)
                        elif selected_axis == Y:
                            ladder.translate_y(sign * 5)
                        elif selected_axis == Z:
                            ladder.translate_z(sign * 5)
                    elif operation == S:
                        if event.key.keysym.sym == SDLK_RIGHT:
                            ladder.plus_scale()
                        else:
                            ladder.minus_scale()
                    elif operation == R:
                        if selected_axis == X:
                            ladder.rotate_x(sign * 5)
                        elif selected_axis == Y:
                            ladder.rotate_y(sign * 5)
                        elif selected_axis == Z:
                            ladder.rotate_z(sign * 5)

        if is_changed:
            is_changed = False
            clear(window_surface)
            draw_projection(pixels, camera, [ladder], adapt_3d_point_to_front_projection)
            window.refresh()

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())