

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def transform(self, options, camera):
        points = [self.a, self.b]
        points = [point.transform(options, camera) for point in points]
        return Edge(points[0], points[1])

    def __getitem__(self, index):
        if index == 0:
            return self.a
        else:
            return self.b

    def __eq__(self, edge):
        return edge.a == self.a and edge.b == self.b or \
            edge.a == self.b and edge.b == self.a

    def __repr__(self):
        return "{0} {1}".format(self.a, self.b)