import random
import time
from glm import vec3
from aabb import AABB
from model import * 

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.skybox = AdvancedSkyBox(app)
        self.first_slenderman_spawned = False 
        self.slenderman = None  
        self.slenderman_timer = time.time()
        self.slenderman_interval = 20.0  
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

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
        while tree_count < 4:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(x - cx) < s / 2 and abs(z - cz) < s / 2:
                    self.add_object(Tree(self.app, pos=(x, -2, z)))
                    self.add_object(Arbol(self.app, pos=(x, -1.2, z)))
                    tree_count += 1
                    break
        self.spawn_slenderman(cube_positions)
    
    def spawn_trees(self, cube_positions):
        tree_count = 0
        n, s = 50, 2
        while tree_count < 4:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            colliding = any(abs(x - cx) < s / 2 and abs(z - cz) < s / 2 for cx, cz in cube_positions)

            if not colliding:
                self.add_object(Tree(self.app, pos=(x, -2, z)))
                self.add_object(Arbol(self.app, pos=(x, -1.2, z))) 
                tree_count += 1

        for obj in self.objects:
            if isinstance(obj, (Tree, Arbol)):
                obj.update_aabb()
    
    def spawn_slenderman(self, cube_positions):
        n, s = 50, 2
        
        if self.first_slenderman_spawned and self.slenderman:
            self.remove_object(self.slenderman)

        while True:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            new_aabb = AABB(vec3(x, -0.3, z) - vec3(0.002/2), vec3(x, -0.3, z) + vec3(0.002/2))
            colliding = any(new_aabb.is_colliding(obj.aabb) for obj in self.objects if obj != self.slenderman)

            if not colliding:
                self.slenderman = Slenderman(self.app, pos=(x, -0.3, z))
                self.add_object(self.slenderman)
                self.first_slenderman_spawned = True  
                break

        self.slenderman_timer = time.time()

    def move_slenderman(self):
        if time.time() - self.slenderman_timer > self.slenderman_interval:
            n, s = 50, 2
            cube_positions = [(cx, cz) for obj in self.objects if isinstance(obj, Cube) for cx, cz in [(obj.pos[0], obj.pos[2])]]

            if self.slenderman:
                self.remove_object(self.slenderman)

            while True:
                x = random.uniform(-n, n)
                z = random.uniform(-n, n)

                new_aabb = AABB(vec3(x, -0.3, z) - vec3(0.002/2), vec3(x, -0.3, z) + vec3(0.002/2))
                colliding = any(new_aabb.is_colliding(obj.aabb) for obj in self.objects if obj != self.slenderman)

                if not colliding:
                    self.slenderman = Slenderman(self.app, pos=(x, -0.3, z))
                    self.add_object(self.slenderman)
                    break

            self.slenderman_timer = time.time()

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self):
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update()  

            if isinstance(obj, (Tree, Slenderman)):
                obj.update_aabb()  

        self.move_slenderman()