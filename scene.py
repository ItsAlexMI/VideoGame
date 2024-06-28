from model import *
import glm
from flashlight import Flashlight


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        n, s = 50, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=(x, -s, z)))

        self.add_object(Tree(self.app, pos=(0, -1, 0)))

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self):
        for obj in self.objects:
            obj.update()