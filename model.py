import moderngl as mgl
import numpy as np
import glm
from aabb import AABB



class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = glm.vec3(pos) 
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = glm.vec3(scale)  
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        self.aabb = self.create_aabb()
        

    def update(self):
        self.m_model = self.get_model_matrix()
        self.update_aabb()

    def get_model_matrix(self):
        m_model = glm.mat4(1.0)  # Identity matrix
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()

    def create_aabb(self):
        min_corner = self.pos - self.scale / 2
        max_corner = self.pos + self.scale / 2
        return AABB(min_corner, max_corner)

    def update_aabb(self):
        self.aabb.min_corner = self.pos - self.scale / 2
        self.aabb.max_corner = self.pos + self.scale / 2


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        # resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        # depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)
        # shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Car(ExtendedBaseModel):
    def __init__(self, app, vao_name='car', tex_id='car', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.create_aabb()

    def create_aabb(self):
        aabb_scale_factor = glm.vec3(7, 10, 7)  
        min_corner = self.pos - (self.scale * aabb_scale_factor) / 2
        max_corner = self.pos + (self.scale * aabb_scale_factor) / 2
        self.aabb = AABB(min_corner, max_corner)

    def update_aabb(self):
        aabb_scale_factor = glm.vec3(7, 10, 7) 
        self.aabb.min_point = self.pos - (self.scale * aabb_scale_factor) / 2
        self.aabb.max_point = self.pos + (self.scale * aabb_scale_factor) / 2

    def update(self):
        super().update()
        self.update_aabb()

class Tree(ExtendedBaseModel):
    def __init__(self, app, vao_name='tree', tex_id='tree', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Grass(ExtendedBaseModel):
    def __init__(self, app, vao_name='grass', tex_id='grass', pos=(0, 0, 0), rot=(0, 0, 0), scale=(0.1, 0.1, 0.1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Rock(ExtendedBaseModel):
    def __init__(self, app, vao_name='rock', tex_id='rock', pos=(0, 0, 0), rot=(0, 0, 0), scale=(0.05, 0.05, 0.05)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Arbol(ExtendedBaseModel):
    def __init__(self, app, vao_name='arbol', tex_id='arbol', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Slenderman(ExtendedBaseModel):
    def __init__(self, app, vao_name='slender', tex_id='slender', pos=(0, 0, 0), rot=(0, 0, 0), scale=(0.002, 0.002, 0.002)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

    def update(self):
        super().update() 

class House(ExtendedBaseModel):
    def __init__(self, app, vao_name='house', tex_id='house', pos=(0, 0, 0), rot=(0, 0, 0), scale=(0.2, 0.2, 0.2)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.create_aabb()

    def create_aabb(self):
        aabb_scale_factor = glm.vec3(285, 1000, 285)  
        min_corner = self.pos - (self.scale * aabb_scale_factor) / 2
        max_corner = self.pos + (self.scale * aabb_scale_factor) / 2
        self.aabb = AABB(min_corner, max_corner)

    def update_aabb(self):
        aabb_scale_factor = glm.vec3(285, 1000, 285) 
        self.aabb.min_point = self.pos - (self.scale * aabb_scale_factor) / 2
        self.aabb.max_point = self.pos + (self.scale * aabb_scale_factor) / 2

    def update(self):
        super().update()
        self.update_aabb()

class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)