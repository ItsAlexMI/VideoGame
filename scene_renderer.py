

class SceneRenderer:
    def __init__(self, app):
        """
        Initializes the SceneRenderer with the given 'app' object.
        """
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        """
        Render the shadow of each object in the scene.

        This function clears the depth buffer and sets it as the current framebuffer.
        Then, it iterates over each object in the scene and calls the `render_shadow()`
        method on each object.
        """
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def main_render(self):
        """
        Renders the main scene by iterating over each object in the scene and calling its `render` method.
        Finally, it renders the skybox.
        """
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def render(self):
        """
        Renders the scene by executing the shadow rendering and main rendering methods sequentially.
        """
        self.render_shadow()
        self.main_render()

    def destroy(self):
        """
        Release the depth framebuffer object.

        This method releases the depth framebuffer object associated with this instance.
        It is used to clean up resources and prevent memory leaks.
        """
        self.depth_fbo.release()

