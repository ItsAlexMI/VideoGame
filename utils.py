from PIL import Image
import os

def extract_frames(gif_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    with Image.open(gif_path) as img:
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_image = img.copy()
            frame_image.save(os.path.join(output_folder, f"frame_{frame}.png"))

gif_path = 'resources\images\menu.gif'
output_folder = 'frames'

extract_frames(gif_path, output_folder)
