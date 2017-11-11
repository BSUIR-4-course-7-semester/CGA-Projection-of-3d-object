import time

import numpy
import sdl2.ext
import sys

import ctypes

from sdl2 import SDL_Point, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_z, SDLK_x, SDLK_y, SDLK_t, SDLK_s, SDLK_r
from sdl2.examples.gui import GREEN
from sdl2.examples.pixelaccess import WHITE, BLACK

from camera import Camera
from drawing import draw_line
from ladder import Ladder
from point import Point3D
from triangle import has_line

FRAME_INTERVAL = sys.maxsize
# FRAME_INTERVAL = 0.2
STEP_COUNT = 2

T = 't'
R = 'r'
S = 's'

X = 'x'
Y = 'y'
Z = 'z'

D_ANGLE = 10
D_DISTANCE = 25


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
    triangles = []

    for figure in figures:
        transform_options = figure.get_transform_options()

        for triangle in figure.triangles:
            tr = triangle.transform(transform_options)
            triangles.append(tr)

        for edge in figure.edges:
            lines.append(edge.transform(transform_options))

    for line in lines:
        draw_line(pixels, line, GREEN, WHITE, triangles)


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
    ladder = Ladder(50, 100, STEP_COUNT)

    operation = R
    selected_axis = Y

    is_changed = True

    last_frame_time = time.time()

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                x, y = ctypes.c_int(0), ctypes.c_int(0)
                sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
                print(x.value, y.value)
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
                            ladder.translate_x(sign * D_DISTANCE)
                        elif selected_axis == Y:
                            ladder.translate_y(sign * D_DISTANCE)
                        elif selected_axis == Z:
                            ladder.translate_z(sign * D_DISTANCE)
                    elif operation == S:
                        if event.key.keysym.sym == SDLK_RIGHT:
                            ladder.plus_scale()
                        else:
                            ladder.minus_scale()
                    elif operation == R:
                        if selected_axis == X:
                            ladder.rotate_x(sign * D_ANGLE)
                        elif selected_axis == Y:
                            ladder.rotate_y(sign * D_ANGLE)
                        elif selected_axis == Z:
                            ladder.rotate_z(sign * D_ANGLE)

        curr_time = time.time()

        if curr_time - last_frame_time > FRAME_INTERVAL:
            ladder.rotate_y(5)
            is_changed = True
            last_frame_time = curr_time

        if is_changed:
            is_changed = False
            clear(window_surface)
            draw_projection(pixels, camera, [ladder], adapt_3d_point_to_up_projection)
            window.refresh()

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())