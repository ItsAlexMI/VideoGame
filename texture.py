import pygame as pg
import moderngl as mgl
import glm


class Texture:
    def __init__(self, app):
        """
        Initializes a Texture object with the given app. The app is used to access the context for rendering.
        This constructor initializes the Texture object by creating and storing textures for various objects.
        The textures are loaded from different image files and stored in the 'textures' dictionary.
        The 'textures' dictionary maps texture names to their corresponding texture objects.
        The constructor also prints the texture object for the 'tree' texture.
        """
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img.png')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox1/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture()
        self.textures['tree'] = self.get_texture(path='objects/pine/nature_bark_pear_01_l_0001.jpg')
        self.textures['grass'] = self.get_texture(path='objects\grass\Grass.png')
        self.textures['rock'] = self.get_texture(path='objects/rock/8b1ab5bc781b40a48fae2331aba07932.jpeg')
        self.textures['arbol'] = self.get_texture(path='objects/arbol/texture_laubbaum.png')
        self.textures['slender'] = self.get_texture(path='objects\slenderman\Tex_0666_0.PNG')
        self.textures['car'] = self.get_texture(path='objects/car/1588147794306-removebg-preview.png')
        self.textures['house'] = self.get_texture(path='objects\house\house_04_diff.png')
    

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        """
        Generate a cube map texture from a set of images stored in a directory.

        Args:
            dir_path (str): Path to the directory containing the images.
            ext (str, optional): File extension of the images. Defaults to 'png'.

        Description:
            This function loads a set of images from a directory and creates a cube map texture object. The images are expected to be named 'right', 'left', 'top', 'bottom', 'front', and 'back'. The images are loaded using Pygame's `image.load()` function and converted to the appropriate format using `convert()`. The images are then flipped horizontally or vertically based on their face, using Pygame's `transform.flip()` function. The resulting textures are stored in a list.

            The function then creates a cube map texture object using the `texture_cube()` function of the current context. The size of the texture is determined by the size of the first loaded image.

            Finally, the function writes the loaded images into the cube map texture object, one face at a time, using the `write()` function of the texture object. The images are converted to a string format using Pygame's `image.tostring()` function.
            The function returns the generated cube map texture object.
        """
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        """
        Load an image from the specified path, flip it horizontally and vertically, and create a texture object with it.
        """
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        """
        Destroy all the textures in the `self.textures` dictionary.

        This function iterates over the values in the `self.textures` dictionary and calls the `release()` method on each texture.
        """
        [tex.release() for tex in self.textures.values()]