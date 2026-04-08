import random
import pyray as pr

from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import circles_collide

SCREEN_W = 800
SCREEN_H = 600
MAX_BULLETS = 5          # limit pociskow

# okno
pr.init_window(SCREEN_W, SCREEN_H, "Asteroids – Lab 07")
pr.set_target_fps(60)

# audio
pr.init_audio_device()

# ladujemy dzwieki
try:
    snd_shoot = pr.load_sound("assets/shoot.wav")
    snd_explode = pr.load_sound("assets/explode.wav")
    has_audio = True
except Exception:
    has_audio = False
    print("Brak plików audio – dźwięki wyłączone.")

# tlo
try:
    bg_texture = pr.load_texture("assets/stars.png")
    has_texture = True
except Exception:
    has_texture = False
    # losowe gwiazdy
    stars = [(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H),
              random.uniform(0.5, 2.0)) for _ in range(200)]

# obiekty
ship = Ship(SCREEN_W / 2, SCREEN_H / 2)
asteroids = [Asteroid(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for _ in range(6)]
bullets: list[Bullet] = []
explosions: list[Explosion] = []

# petla gry
while not pr.window_should_close():
    dt = pr.get_frame_time()

    # update
    ship.update(dt)

    # strzelanie
    if pr.is_key_pressed(pr.KEY_SPACE) and len(bullets) < MAX_BULLETS:
        nose_x = ship.pos.x + 20 * __import__("math").sin(ship.angle)
        nose_y = ship.pos.y - 20 * __import__("math").cos(ship.angle)
        bullets.append(Bullet(nose_x, nose_y, ship.angle))
        if has_audio:
            pr.play_sound(snd_shoot)

    for b in bullets:
        b.update(dt)
    for a in asteroids:
        a.update(dt)
    for e in explosions:
        e.update(dt)

    # kolizje pociskow
    for b in bullets:
        if not b.alive:
            continue
        for a in asteroids:
            if not a.alive:
                continue
            if circles_collide(b.x, b.y, b.radius, a.pos.x, a.pos.y, a.radius):
                b.alive = False
                a.alive = False
                explosions.append(Explosion(a.pos.x, a.pos.y, a.radius * 1.5))
                if has_audio:
                    pr.play_sound(snd_explode)

    # kolizja statku
    for a in asteroids:
        if not a.alive:
            continue
        if circles_collide(ship.pos.x, ship.pos.y, 15, a.pos.x, a.pos.y, a.radius):
            a.alive = False
            explosions.append(Explosion(ship.pos.x, ship.pos.y, 30))
            if has_audio:
                pr.play_sound(snd_explode)
            # reset
            ship.pos.x, ship.pos.y = SCREEN_W / 2, SCREEN_H / 2
            ship.vel.x, ship.vel.y = 0.0, 0.0

    # czyszczenie list
    bullets = [b for b in bullets if b.alive]
    asteroids = [a for a in asteroids if a.alive]
    explosions = [e for e in explosions if e.alive]

    # rysowanie
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # rysowanie tla
    if has_texture:
        pr.draw_texture(bg_texture, 0, 0, pr.WHITE)
    else:
        for sx, sy, sr in stars:
            pr.draw_circle(int(sx), int(sy), sr, pr.RAYWHITE)

    # reszta obiektow
    for a in asteroids:
        a.draw()
    for b in bullets:
        b.draw()
    for e in explosions:
        e.draw()
    ship.draw()

    # HUD
    pr.draw_text(f"Pociski: {len(bullets)}/{MAX_BULLETS}", 10, 10, 18, pr.GREEN)
    pr.draw_text(f"Asteroidy: {len(asteroids)}", 10, 32, 18, pr.GREEN)

    pr.end_drawing()

# zwalnianie pamieci
if has_audio:
    pr.unload_sound(snd_shoot)
    pr.unload_sound(snd_explode)
    pr.close_audio_device()

if has_texture:
    pr.unload_texture(bg_texture)

pr.close_window()