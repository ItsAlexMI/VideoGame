# flashligh.py
import glm

class Flashlight:
    def __init__(self, app):
        self.app = app
        self.position = glm.vec3(0, 0, 0)  # Inicialmente debajo de la cámara
        self.color = glm.vec3(1, 1, 1)  # Color blanco por defecto
        self.angle = glm.radians(35)  # Ángulo de luz de 35 grados
        self.Ia = 5.0 * self.color  # Intensidad ambiental (igual a la luz ambiental existente)
        self.Id = 5.0 * self.color  # Intensidad difusa
        self.Is = 5.0 * self.color  # Intensidad especular
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.app.camera.forward, glm.vec3(0, 1, 0))

    def update(self):
        self.position = self.app.camera.position - glm.vec3(0, 0.5, 0)  # Actualiza la posición debajo de la cámara
        self.m_view_light = self.get_view_matrix()

    def get_direction(self):
        return self.app.camera.forward
