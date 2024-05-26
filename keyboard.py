from libraries import *

# Variables de estado para el movimiento continuo
move_left = False
move_right = False
move_forward = False
move_backward = False
move_up = False
move_down = False


# Velocidad del movimiento
move_speed = 0.1

def key_callback(window, key, scancode, action, mods):
    global move_left, move_right, move_forward, move_backward, move_up, move_down
    
    if action == glfw.PRESS:
        if key == glfw.KEY_A:
            move_left = True
        elif key == glfw.KEY_D:
            move_right = True
        elif key == glfw.KEY_W:
            move_forward = True
        elif key == glfw.KEY_S:
            move_backward = True
        elif key == glfw.KEY_SPACE:
            move_up = True
        elif key == glfw.KEY_LEFT_SHIFT:
            move_down = True
    elif action == glfw.RELEASE:
        if key == glfw.KEY_A:
            move_left = False
        elif key == glfw.KEY_D:
            move_right = False
        elif key == glfw.KEY_W:
            move_forward = False
        elif key == glfw.KEY_S:
            move_backward = False
        elif key == glfw.KEY_SPACE:
            move_up = False
        elif key == glfw.KEY_LEFT_SHIFT:
            move_down = False

def continue_state():
    if move_left:
            glTranslatef(move_speed, 0, 0)
    if move_right:
        glTranslatef(-move_speed, 0, 0)
    if move_forward:
        glTranslatef(0, 0, move_speed)
    if move_backward:
        glTranslatef(0, 0, -move_speed)
    if move_up:
        glTranslatef(0, -move_speed, 0)
    if move_down:
        glTranslatef(0, move_speed, 0)