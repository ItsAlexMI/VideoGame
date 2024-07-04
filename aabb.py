import glm

class AABB:
    def __init__(self, min_point, max_point):
        """
        Initializes the AABB object with the minimum and maximum points.
        """
        self.min_point = glm.vec3(min_point)
        self.max_point = glm.vec3(max_point)

    def is_colliding(self, other):
        """
        Check if this AABB is colliding with another AABB.
        """
        return (self.min_point.x <= other.max_point.x and self.max_point.x >= other.min_point.x) and \
               (self.min_point.y <= other.max_point.y and self.max_point.y >= other.min_point.y) and \
               (self.min_point.z <= other.max_point.z and self.max_point.z >= other.min_point.z)

