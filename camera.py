import glm
import pygame as pg
import math
import time
from aabb import AABB
from model import *
from videos import *

FOV = 50  
NEAR = 0.1
FAR = 100
SPEED = 0.005
SENSITIVITY = 0.03

class Camera:
    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
        """
        Initializes a new instance of the Camera class.

        Args:
            app (App): The application instance.
            position (tuple, optional): The initial position of the camera. Defaults to (0, 0, 4).
            yaw (float, optional): The initial yaw angle of the camera. Defaults to -90.
            pitch (float, optional): The initial pitch angle of the camera. Defaults to 0.
        """
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.size = glm.vec3(1, 2, 1) 
        self.aabb = AABB(self.position - self.size / 2, self.position + self.size / 2)

        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

        self.is_jumping = False
        self.jump_start_time = None
        self.jump_start_y = 0.0

        self.move_sound = pg.mixer.Sound('resources/sounds/pasos.wav')
        self.move_sound.set_volume(1.5)  
        self.jump_sound = pg.mixer.Sound('resources/sounds/jump.wav')
        self.jump_sound.set_volume(0.5)  
        self.is_moving = False

        self.screamer_played = False
        self.final_played = False
    def rotate(self):
        """
        Updates the yaw and pitch angles based on the relative mouse movement.
        """
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        """
        This function calculates the forward, right, and up vectors of the camera based on the current yaw and pitch angles.
        It uses the glm library to perform the calculations.
        """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        """
        This function first calls the `move` method to update the camera's position based on user input.
        Then, it calls the `rotate` method to update the camera's yaw and pitch angles based on the relative mouse movement.
        After that, it calls the `update_camera_vectors` method to recalculate the camera's forward, right, and up vectors based on the updated yaw and pitch angles.
        Finally, it calls the `get_view_matrix` method to update the camera's view matrix based on its position, rotation, and other properties.
        """
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
            velocity = SPEED * self.app.delta_time
            keys = pg.key.get_pressed()

            move_dir = glm.vec3(0)

            forward_dir = glm.vec3(self.forward.x, 0, self.forward.z)
            if keys[pg.K_w]:
                move_dir += forward_dir
            if keys[pg.K_s]:
                move_dir -= forward_dir

            if keys[pg.K_a]:
                move_dir -= self.right
            if keys[pg.K_d]:
                move_dir += self.right

            if glm.length(move_dir) > 0:
                move_dir = glm.normalize(move_dir) * velocity
                new_position = self.position + move_dir
                new_aabb = AABB(new_position - self.size / 2, new_position + self.size / 2)
                if not self.check_collisions(new_aabb):
                    self.position = new_position
                    self.aabb = new_aabb
                    if not self.is_moving:
                        self.move_sound.play(-1)
                        self.is_moving = True
                else:
                    if self.is_moving:
                        self.move_sound.stop()
                        self.is_moving = False
            else:
                if self.is_moving:
                    self.move_sound.stop()
                    self.is_moving = False

            if keys[pg.K_SPACE] and not self.is_jumping:
                self.is_jumping = True
                self.jump_start_y = self.position.y
                self.jump_start_time = time.time()
                self.jump_sound.play()

            if self.is_jumping:
                jump_duration = 0.7
                jump_progress = (time.time() - self.jump_start_time) / jump_duration

                if jump_progress <= 1.0:
                    jump_height = 2.0
                    self.position.y = self.jump_start_y + jump_height * math.sin(jump_progress * math.pi)
                    self.position += move_dir * velocity
                else:
                    self.is_jumping = False
                    self.jump_start_time = None
            else:
                gravity = 9.8
                ground_level = 0.0

                if self.position.y > ground_level:
                    self.position.y -= gravity * velocity
                    if self.position.y < ground_level:
                        self.position.y = ground_level

    def check_collisions(self, aabb):
        """
        Checks for collisions between the player's AABB and specific objects in the scene.
        """
        for obj in self.app.scene.objects:
            if isinstance(obj, (Slenderman, Car, House)):
                if aabb.is_colliding(obj.aabb):
                    print("Colision " + obj.__class__.__name__)
                    if isinstance(obj, Slenderman):
                        self.screamer_played = True
                        pg.quit()
                        play_screamer()
                        sys.exit()
                        
                    if isinstance(obj, Car):
                        self.final_played = True
                        pg.quit()
                        play_final()
                        sys.exit()
                    return True

                    

        return False


    def get_view_matrix(self):
        """
        Returns the view matrix for the camera.

        This function calculates the view matrix for the camera based on its position, forward vector, and up vector.
        It uses the `glm.lookAt` function to compute the view matrix.
        """
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        """
        This function calculates the projection matrix for the camera based on the field of view (FOV), aspect ratio, near plane distance, and far plane distance.
        """
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_flashlight_position(self):
        """
        This function calculates the flashlight's position based on the camera's position, forward vector, and a fixed offset.
        """
        return self.position + self.forward * glm.vec3(0, 0, -1)