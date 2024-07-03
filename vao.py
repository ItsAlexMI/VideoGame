from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, ctx):
        """
        Initializes a new instance of the VAO class.
        """
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        self.setup_vaos()

    def setup_vaos(self):
        """
        Initializes the VAOs for various objects and skyboxes.

        This function sets up the vertex array objects (VAOs) for different objects
        such as 'cube', 'tree', 'grass', 'arbol', 'rock', 'slender', 'shadow_cube',
        'shadow_arbol', 'shadow_grass', 'shadow_tree', 'shadow_rock', 'shadow_slender',
        'skybox', and 'advanced_skybox'. Each VAO is associated with a specific shader
        program and vertex buffer object (VBO).
        """
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube'])

        self.vaos['tree'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['tree'])

        self.vaos['grass'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['grass'])    

        self.vaos['arbol'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['arbol'])    

        self.vaos['rock'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['rock'])

        self.vaos['slender'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['slender'])

        self.vaos['car'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['car'])

        self.vaos['house'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['house'])

        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube'])
        
        self.vaos['shadow_arbol'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['arbol'])

        self.vaos['shadow_grass'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['grass'])  

        self.vaos['shadow_tree'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['tree'])


        self.vaos['shadow_rock'] = self.get_vao(
        program=self.program.programs['shadow_map'],
        vbo=self.vbo.vbos['rock'])

        self.vaos['shadow_slender'] = self.get_vao(
        program=self.program.programs['shadow_map'],
        vbo=self.vbo.vbos['slender'])

        self.vaos['shadow_car'] = self.get_vao(
        program=self.program.programs['shadow_map'],
        vbo=self.vbo.vbos['car'])


        self.vaos['shadow_house'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['house'])

        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        """
        Creates a vertex array object (VAO) using the provided program and vertex buffer object (VBO).

        Parameters:
            program (Program): The program to be used for rendering.
            vbo (VertexBufferObject): The VBO containing the vertex data.
        """
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        """
        Destroys the VAO by releasing the associated VBO and program.
        This function calls the `destroy()` method on the `vbo` and `program` attributes of the current instance.
        """
        self.vbo.destroy()
        self.program.destroy()