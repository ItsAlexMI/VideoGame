from vao import VAO
from texture import Texture


class Mesh:
    def __init__(self, app):
        """
        Initializes the Mesh object with the given 'app' object.
        """
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app)

    def destroy(self):
        """
        Destroys the mesh by releasing the associated vertex array object (VAO) and texture.

        This function calls the `destroy()` method on the `vao` and `texture` attributes of the current instance.
        """
        self.vao.destroy()
        self.texture.destroy()