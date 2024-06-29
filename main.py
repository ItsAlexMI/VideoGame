import pygame as pg
from pygame import mixer
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from shader_program import ShaderProgram

class GraphicsEngine:
    def __init__(self, win_size=(1080, 1024), fullscreen=True):
        pg.init()
        mixer.init()
        mixer.music.load('resources/sounds/ambient.wav')
        mixer.music.set_volume(0.2)

        self.WIN_SIZE = win_size
        self.fullscreen = fullscreen

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        if self.fullscreen:
            flags = pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN
        else:
            flags = pg.OPENGL | pg.DOUBLEBUF

        self.screen = pg.display.set_mode(self.WIN_SIZE, flags)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)
        self.shader_program = ShaderProgram(self.ctx)  

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                self.shader_program.destroy()  
                mixer.music.stop()  
                pg.quit()
                sys.exit()

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene_renderer.render()

        shader_program = self.shader_program.programs['default']


        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        mixer.music.play(loops=-1) 
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.scene.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
