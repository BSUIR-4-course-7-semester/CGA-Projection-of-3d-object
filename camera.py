class Camera:
    def __init__(self, width, height, front_distance, back_distance):
        self.width = int(width / 2)
        self.height = int(height / 2)
        self.front_distance = front_distance
        self.back_distance = back_distance

        q = back_distance / (back_distance - front_distance)

        self.projection_matrix = [
            [width, 0, 0, 0],
            [0, height, 0, 0],
            [0, 0, q, 1],
            [0, 0, -q * front_distance, 0]
        ]
