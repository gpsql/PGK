import pyray as pr
from pathlib import Path
import os

print(f"Current Working Directory: {os.getcwd()}")
script_dir = Path(__file__).parent
print(f"Script Directory: {script_dir}")

pr.init_window(100, 100, "Test")
pr.init_audio_device()

shoot_path = "assets/shoot.wav"
explode_path = "assets/explode.wav"

print(f"Checking {shoot_path}: {os.path.exists(shoot_path)}")
print(f"Checking {explode_path}: {os.path.exists(explode_path)}")

snd_shoot = pr.load_sound(shoot_path)
snd_explode = pr.load_sound(explode_path)

print(f"Is shoot ready? {pr.is_sound_ready(snd_shoot)}")
print(f"Is explode ready? {pr.is_sound_ready(snd_explode)}")

pr.unload_sound(snd_shoot)
pr.unload_sound(snd_explode)
pr.close_audio_device()
pr.close_window()
