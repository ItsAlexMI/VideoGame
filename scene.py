from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        n, s = 10, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=(x, -s, z)))

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self):
        for obj in self.objects:
            obj.update()