import numpy as np

class AABB:
    def __init__(self, min_corner, max_corner):
        self.min_corner = np.array(min_corner)
        self.max_corner = np.array(max_corner)

    def is_colliding(self, other):
        return (self.min_corner[0] <= other.max_corner[0] and
                self.max_corner[0] >= other.min_corner[0] and
                self.min_corner[1] <= other.max_corner[1] and
                self.max_corner[1] >= other.min_corner[1] and
                self.min_corner[2] <= other.max_corner[2] and
                self.max_corner[2] >= other.min_corner[2])
