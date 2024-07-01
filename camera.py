import glm
import pygame as pg
import math
import time
from aabb import AABB
from model import *

FOV = 50  
NEAR = 0.1
FAR = 100
SPEED = 0.005
SENSITIVITY = 0.03

class Camera:
    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
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

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
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

            # Verifica colisiones antes de aplicar el movimiento
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
        for obj in self.app.scene.objects:
            if isinstance(obj, (Tree, Slenderman)):
                if aabb.is_colliding(obj.aabb):
                    return True
        return False

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_flashlight_position(self):
        return self.position + self.forward * glm.vec3(0, 0, -1)