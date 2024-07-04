import glm

class Light:
    def __init__(self, position=(10, 50, 50), color=(1, 1, 1)):
        """
        Initialize the Light object with the specified position and color. 
        Set the direction to the default (0, 0, 0). 
        Calculate and assign the ambient, diffuse, and specular intensities. 
        Compute the view matrix using the get_view_matrix method and assign it to m_view_light.
        """
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(0, 0, 0)
        # intensities
        self.Ia = 0 * self.color  # ambient
        self.Id = 0.001 * self.color  # diffuse
        self.Is = 0.04 * self.color  # specular
        # view matrix
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))