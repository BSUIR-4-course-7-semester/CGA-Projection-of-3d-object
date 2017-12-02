import numpy as np


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.p = 0.005

    def get_projection_matrix(self):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, self.p],
            [0, 0, 0, 1]
        ])

    def change_p(self, dp):
        self.p += dp
        if self.p < 0.005:
            self.p = 0.005

