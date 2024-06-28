from model import *
import glm
import random

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
        grass_density = 4
        rock_count = 3  
        cube_positions = []
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=(x, -s, z)))
                cube_positions.append((x, z))

                for _ in range(grass_density):
                    grass_x = random.uniform(x - s/2, x + s/2)
                    grass_z = random.uniform(z - s/2, z + s/2)
                    self.add_object(Grass(self.app, pos=(grass_x, -1.3, grass_z)))
        
        rocks_generated = 0
        while rocks_generated < rock_count:
            rock_x = random.uniform(-n, n)
            rock_z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(rock_x - cx) < s / 2 and abs(rock_z - cz) < s / 2:
                    self.add_object(Rock(self.app, pos=(rock_x, -1, rock_z)))
                    rocks_generated += 1
                    break

        tree_count = 0
        while tree_count < 2:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(x - cx) < s / 2 and abs(z - cz) < s / 2:
                    self.add_object(Tree(self.app, pos=(x, -3, z)))
                    tree_count += 1
                    break


    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self):
        for obj in self.objects:
            obj.update()
