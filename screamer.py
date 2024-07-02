import pygame as pg
from pyvidplayer import Video
import time
import subprocess
import sys

def play_screamer():
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    screamer = Video("resources/images/screamer.mp4")
    screamer.set_size((screen.get_width(), screen.get_height()))

    start_time = time.time()
    while time.time() - start_time < 7:
        screen.fill((0, 0, 0))
        screamer.draw(screen, (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                screamer.close()
                pg.quit()
                sys.exit()

    screamer.close()
    pg.quit()
    subprocess.run([sys.executable, "menu.py"])
    sys.exit()

if __name__ == '__main__':
    play_screamer()
