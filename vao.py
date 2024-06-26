from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # Configuración de los VAOs
        self.setup_vaos()

    def setup_vaos(self):
        # VAO para el cubo
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube'])

        # VAO para el árbol
        self.vaos['tree'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['tree'])

        # VAO para la sombra del cubo
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube'])

        # VAO para la sombra del árbol
        self.vaos['shadow_tree'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['tree'])

        # VAO para el skybox
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # VAO para el skybox avanzado
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
