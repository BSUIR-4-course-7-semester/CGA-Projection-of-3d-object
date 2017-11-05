class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def to_lines(self):
        return [
            [self.a, self.b],
            [self.b, self.c],
            [self.c, self.a]
        ]

    def transform(self, options):
        points = [self.a, self.b, self.c]
        points = [point.transform(options) for point in points]
        return Triangle(points[0], points[1], points[2])