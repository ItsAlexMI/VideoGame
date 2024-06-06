from libraries import *

class Texture:
    def __init__(self, image, texType, slot, format, pixelType):
        self.type = texType
        self.id = glGenTextures(1)
        glActiveTexture(slot)
        glBindTexture(texType, self.id)

        glTexParameteri(texType, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(texType, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(texType, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(texType, GL_TEXTURE_WRAP_T, GL_REPEAT)

        image = Image.open(image)
        image_data = image.convert("RGBA").tobytes()
        width, height = image.size

        glTexImage2D(texType, 0, GL_RGBA, width, height, 0, format, pixelType, image_data)
        glGenerateMipmap(texType)

        glBindTexture(texType, 0)

    def Bind(self):
        glBindTexture(self.type, self.id)

    def Unbind(self):
        glBindTexture(self.type, 0)

    def Delete(self):
        glDeleteTextures(1, [self.id])
