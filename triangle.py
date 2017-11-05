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