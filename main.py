import glfw
import glm
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from libraries import *





def main():
    if not glfw.init():
        return

    width, height = 800, 600
    window = glfw.create_window(width, height, "OpenGL Window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    camera = Camera(width, height, glm.vec3(0.0, -3.0, 3.0))  # Movemos la cámara hacia abajo

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(0.0, -3.0, 3.0, 0.0)  
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -10)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        continue_state(camera)
        camera.Inputs(window)
        camera.updateMatrix(45, 0.1, 100)  # Actualizamos la matriz de la cámara

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Convert the camera matrix to a format suitable for OpenGL
        camera_matrix_flat = np.array(camera.cameraMatrix, dtype=np.float32)
        camera_matrix_flat = np.transpose(camera_matrix_flat)

        # Load the camera matrix into OpenGL
        glLoadMatrixf(camera_matrix_flat)

        
        num_cubes_x = 20  # Número de cubos en el eje x
        num_cubes_z = 20  # Número de cubos en el eje z
        cube_spacing = 1.5  # Espacio entre los cubos

        for i in range(num_cubes_x):
            for j in range(num_cubes_z):
                x = i * cube_spacing
                z = j * cube_spacing
                draw_cube(x, 0, z)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
