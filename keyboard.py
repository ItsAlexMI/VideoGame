from libraries import *
import glfw
import glm
from OpenGL.GL import *

# Variables de estado para el movimiento continuo
move_left = False
move_right = False
move_forward = False
move_backward = False
move_up = False
move_down = False

# Velocidad del movimiento
move_speed = 0.1

class Camera:
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        self.Position = position
        self.Orientation = glm.vec3(0.0, 0.0, -1.0)
        self.Up = glm.vec3(0.0, 1.0, 0.0)
        self.cameraMatrix = glm.mat4(1.0)
        self.speed = 0.1
        self.sensitivity = 100.0
        self.firstClick = True

    def updateMatrix(self, FOVdeg, nearPlane, farPlane):
        view = glm.lookAt(self.Position, self.Position + self.Orientation, self.Up)
        projection = glm.perspective(glm.radians(FOVdeg), self.width / self.height, nearPlane, farPlane)
        self.cameraMatrix = projection * view

    def Inputs(self, window):
        global move_left, move_right, move_forward, move_backward, move_up, move_down
        
        if move_forward:
            self.Position += self.speed * self.Orientation
        if move_backward:
            self.Position -= self.speed * self.Orientation
        if move_left:
            self.Position -= glm.normalize(glm.cross(self.Orientation, self.Up)) * self.speed
        if move_right:
            self.Position += glm.normalize(glm.cross(self.Orientation, self.Up)) * self.speed
        if move_up:
            self.Position += self.speed * self.Up
        if move_down:
            self.Position -= self.speed * self.Up

        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
            if self.firstClick:
                glfw.set_cursor_pos(window, self.width / 2, self.height / 2)
                self.firstClick = False

            mouseX, mouseY = glfw.get_cursor_pos(window)
            rotX = self.sensitivity * float(mouseY - self.height / 2) / self.height
            rotY = self.sensitivity * float(mouseX - self.width / 2) / self.width

            newOrientation = glm.rotate(self.Orientation, glm.radians(-rotX), glm.normalize(glm.cross(self.Orientation, self.Up)))
            angle = glm.angleAxis(glm.dot(newOrientation, self.Up), glm.cross(newOrientation, self.Up))

            if glm.length(angle) <= glm.radians(85.0):

                self.Orientation = newOrientation

            self.Orientation = glm.rotate(self.Orientation, glm.radians(-rotY), self.Up)
            glfw.set_cursor_pos(window, self.width / 2, self.height / 2)
        elif glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.RELEASE:
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            self.firstClick = True

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

def continue_state(camera):
    if move_left:
        camera.Position -= glm.normalize(glm.cross(camera.Orientation, camera.Up)) * move_speed
    if move_right:
        camera.Position += glm.normalize(glm.cross(camera.Orientation, camera.Up)) * move_speed
    if move_forward:
        camera.Position += camera.Orientation * move_speed
    if move_backward:
        camera.Position -= camera.Orientation * move_speed
    if move_up:
        camera.Position += camera.Up * move_speed
    if move_down:
        camera.Position -= camera.Up * move_speed