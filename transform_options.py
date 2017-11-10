class TransformOptions:
    def __init__(self, x_angle, y_angle, z_angle, scale, dx, dy, dz):
        self.x_angle = x_angle
        self.y_angle = y_angle
        self.z_angle = z_angle
        self.scale = scale
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def __repr__(self):
        return "{0} {1} {2} {3} {4}".format(self.dx, self.dy, self.x_angle, self.y_angle, self.z_angle)