import pygame
import sys
import subprocess
import os
import random
import time

def load_frames(folder):
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder, filename))
            frames.append(frame)
    return frames

def menu(output_folder):
    pygame.init()
    pygame.mixer.init()  
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Menu")

    frames = load_frames(output_folder)
    num_frames = len(frames)
    frame_index = 0

    screen_width, screen_height = screen.get_size()

    click_sound = pygame.mixer.Sound('resources/sounds/click.wav')
    hover_sound = pygame.mixer.Sound('resources/sounds/hover.wav')

    click_sound.set_volume(1.0)
    hover_sound.set_volume(1.0)

    hover_channel = pygame.mixer.Channel(0)
    click_channel = pygame.mixer.Channel(1)

    clock = pygame.time.Clock()

    play_hovered = False
    exit_hovered = False

    title_font = pygame.font.Font('resources/fonts/HorrorFont-Regular.ttf', 130)
    button_font = pygame.font.Font('resources/fonts/HorrorFont-Regular.ttf', 50)

    play_button_bg_img = pygame.image.load('resources/images/image.png').convert_alpha()
    exit_button_bg_img = pygame.image.load('resources/images/image.png').convert_alpha()

    play_button_bg_img = pygame.transform.scale(play_button_bg_img, (320, 100)) 
    exit_button_bg_img = pygame.transform.scale(exit_button_bg_img, (320, 100)) 

    title_text = "OUT OF THE WOODS"
    title_text_render = title_font.render(title_text, True, (255, 255, 255))
    title_text_rect = title_text_render.get_rect(center=(screen_width // 2, screen_height // 4))

    max_glitch_offset = 20 

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        screen.blit(frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % num_frames

        glitch_x = title_text_rect.x + random.randint(-max_glitch_offset, max_glitch_offset)
        glitch_y = title_text_rect.y + random.randint(-max_glitch_offset, max_glitch_offset)
        screen.blit(title_text_render, (glitch_x, glitch_y))

        button_width, button_height = 320, 100 
        button_margin = 80  
        button_x = (screen_width - button_width) // 2
        button_y_play = (screen_height - button_height - button_margin) // 2
        button_y_exit = button_y_play + button_height + button_margin

        play_button = pygame.Rect(button_x, button_y_play, button_width, button_height)
        exit_button = pygame.Rect(button_x, button_y_exit, button_width, button_height)

        def draw_button(button, text, background_img, mouse_over):
            text_color = (255, 255, 255)

            button_text = button_font.render(text, True, text_color)
            text_rect = button_text.get_rect(center=button.center)

            if mouse_over:
                screen.blit(background_img, button)

            screen.blit(button_text, text_rect)

        play_mouse_over = play_button.collidepoint(mouse_pos)
        exit_mouse_over = exit_button.collidepoint(mouse_pos)

        if play_mouse_over and not play_hovered:
            hover_channel.play(hover_sound)
            play_hovered = True
        elif not play_mouse_over:
            play_hovered = False

        if exit_mouse_over and not exit_hovered:
            hover_channel.play(hover_sound)
            exit_hovered = True
        elif not exit_mouse_over:
            exit_hovered = False

        if play_mouse_over and mouse_click:
            click_channel.play(click_sound)
            try:
                subprocess.run([sys.executable, "main.py"], check=True)
                pygame.quit()
                sys.exit()
            except subprocess.CalledProcessError as e:
                print(f"Error running main.py: {e}")

        if exit_mouse_over and mouse_click:
            click_channel.play(click_sound)
            time.sleep(4)
            pygame.quit()
            sys.exit()

        draw_button(play_button, "JUGAR", play_button_bg_img, play_mouse_over)
        draw_button(exit_button, "SALIR", exit_button_bg_img, exit_mouse_over)

        pygame.display.flip()

        clock.tick(120) 

if __name__ == "__main__":
    output_folder = 'frames'
    menu(output_folder)
