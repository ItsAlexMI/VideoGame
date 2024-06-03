import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

def load_texture(image_path):
    try:
        texture_surface = pygame.image.load(image_path)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        return texture_id

    except Exception as e:
        print(f"Error al cargar la textura: {e}")
        return 0

def draw_background(texture_id, width, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -1)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def main():
    pygame.init()

    width, height = 800, 600
    display = (width, height)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -10)

    background_texture = load_texture('./resource/fondo.png')  # Cambia esto a la ruta de tu imagen

    if background_texture == 0:
        print("Error: No se pudo cargar la textura de fondo.")
        return
    else:
        print(f"Textura cargada correctamente con ID: {background_texture}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background(background_texture, width, height)
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
