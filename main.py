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

    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    while not glfw.window_should_close(window):
        glfw.poll_events()

       
        continue_state()
       
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
