import random
import time
from glm import vec3
from aabb import AABB
from model import *

class Scene:
    def __init__(self, app):
        """
        Initializes a new instance of the Scene class.
        """
        self.app = app
        self.objects = []
        self.skybox = AdvancedSkyBox(app)
        self.first_slenderman_spawned = False 
        self.slenderman = None  
        self.slenderman_timer = time.time()
        self.slenderman_interval = 5.0  
        self.load()

    def add_object(self, obj):
        """
        Adds an object to the list of objects in the scene.
        """
        self.objects.append(obj)

    def remove_object(self, obj):
        """
        Removes an object from the list of objects in the scene.
        """
        if obj in self.objects:
            self.objects.remove(obj)

    def load(self):
        """
        Initializes the scene by creating a grid of cubes, grass, rocks, and trees.
        
        This function creates a grid of cubes with a size of `n` by `n` with a spacing of `s`. 
        It then randomly generates grass objects within the grid with a density of `grass_density`.
        It also randomly generates rock objects within the grid, ensuring that they do not overlap with the cubes.
        Finally, it randomly generates tree objects within the grid, ensuring that they do not overlap with the cubes.
        """
        n, s = 100, 2    
        grass_density = 1
   
        cube_positions = []

        for x in range(-n, n, s):
            for z in range(-n, n, s):
                self.add_object(Cube(self.app, pos=(x, -s, z)))
                cube_positions.append((x, z))

                for _ in range(grass_density):
                    grass_x = random.uniform(x - s/2, x + s/2)
                    grass_z = random.uniform(z - s/2, z + s/2)
                    self.add_object(Grass(self.app, pos=(grass_x, -1.3, grass_z)))

        self.spawn_trees(cube_positions)
        self.spawn_rocks(cube_positions)
        self.spawn_house(cube_positions)
        self.spawn_palitos(cube_positions)
        self.spawn_slenderman(cube_positions)
    
    def spawn_trees(self, cube_positions):
        """
        Spawns trees in the scene without overlapping with other objects.
        """
        tree_count = 0
        n, s = 80, 2
        while tree_count < 400:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(x - cx) < s / 2 and abs(z - cz) < s / 2:
                    self.add_object(Arbol(self.app, pos=(x + random.uniform(10, 30), -1.2, z + random.uniform(10, 30))))
                    tree_count += 1
                    break

    def spawn_palitos(self, cube_positions):
        """
        Spawns palitos in the scene without overlapping with other objects.
        """
        tree_count = 0
        n, s = 50, 2
        while tree_count < 30:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(x - cx) < s / 2 and abs(z - cz) < s / 2:
                    self.add_object(Tree(self.app, pos=(x, -1,z)))
                    tree_count += 1
                    break

    def spawn_rocks(self, cube_positions):
        """
        Spawns rocks in the scene without overlapping with other objects.
        """
        rock_count = 0
        n, s = 50, 2
        while rock_count < 30:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(x - cx) < s / 2 and abs(z - cz) < s / 2:
                    self.add_object(Rock(self.app, pos=(x + random.uniform(10, 30), -1, z + random.uniform(10, 30))))
                    rock_count += 1
                    break

    def spawn_house(self, cube_positions):
        """
        Spawns a house in the scene without overlapping with other objects.
        """
        tree_count = 0
        n, s = 50, 2
        
        car_x = random.uniform(-n, n)
        car_z = random.uniform(-n, n)
        for cx, cz in cube_positions:
            if abs(car_x - cx) < s / 2 and abs(car_z - cz) < s / 2:
                car_x = random.uniform(-n, n)
                car_z = random.uniform(-n, n)
                break
        while tree_count < 1:
            x = random.uniform(-n, n)
            z = random.uniform(-n, n)

            for cx, cz in cube_positions:
                if abs(x - cx) < s / 2 and abs(z - cz) < s / 2:
                    self.add_object(Car(self.app, pos=(car_x, -1, car_z), rot=(0, 0, 0), scale=(0.7, 0.7, 0.7)))
                    self.add_object(House(self.app, pos=(car_x + 7, -1, car_z + 7), rot=(0, 0, 0), scale=(0.05, 0.05, 0.05)))                    
                    tree_count += 1
                    break

    def spawn_slenderman(self, cube_positions):
        """
        Spawns a Slenderman in the scene without overlapping with other objects.
        """
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
        """
        Moves the Slenderman in the scene at a random position without overlapping with other objects.

        This function checks if enough time has passed since the last movement of the Slenderman. If it has,
        it generates a new random position for the Slenderman within a range of -n to n in the x and z
        coordinates. It then creates a new Axis-Aligned Bounding Box (AABB) for the new position and checks
        if it collides with any other objects in the scene. If it does not collide, the Slenderman is
        removed from the scene and a new Slenderman is created at the new position. The timer for the
        Slenderman's movement is updated.
        """
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
        """
        Renders all objects in the scene and the skybox.
        This function iterates over each object in the `self.objects` list and calls its `render` method. This allows each object to render itself on the screen. After rendering all the objects, the `render` method of the `self.skybox` object is called to render the skybox.
        """
        for obj in self.objects:
            obj.render()
        self.skybox.render()

    def update(self):
        """
        Updates each object in the scene, checking if they have an `update` method and calling it if present.
        If the object is an instance of `Tree` or `Slenderman`, updates their Axis-Aligned Bounding Box (AABB).
        Finally, moves the Slenderman in the scene to a new random position.
        """
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update()  

            if isinstance(obj, (Tree, Slenderman)):
                obj.update_aabb()  

        self.move_slenderman()
