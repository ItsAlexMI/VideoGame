from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube',
            color=color.color(255, 255, 255),
            highlight_color=color.azure,
            **kwargs
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.position + mouse.normal)
            if key == 'right mouse down':
                destroy(self)



for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()



sky = Sky()

app.run()
