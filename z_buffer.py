import numpy


class ZBuffer:
    def __init__(self, width, height):
        self.surface = numpy.empty([width, height])
