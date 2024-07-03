class ShaderProgram:
    def __init__(self, ctx):
        """
        Initializes a new instance of the ShaderProgram class.

        Initializes the following attributes:
            - ctx (Context): The context object used to create the shader programs.
            - programs (dict): A dictionary that maps shader program names to their corresponding shader programs.
        """
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['skybox'] = self.get_program('skybox')
        self.programs['advanced_skybox'] = self.get_program('advanced_skybox')
        self.programs['shadow_map'] = self.get_program('shadow_map')

    def get_program(self, shader_program_name):
        """
        Initializes a shader program by reading the vertex and fragment shaders from files.
        """
        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        """
        Destroys all the shader programs in the `self.programs` dictionary.

        This function iterates over the values in the `self.programs` dictionary and calls the `release()` method on each program.
        """
        [program.release() for program in self.programs.values()]
