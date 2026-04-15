"""
Asteroids – Lab 08
FSM: MENU → GAME → GAME_OVER
Bonus: fale asteroid (*), zapis najlepszego wyniku (**)
"""

import math
import random
from enum import Enum
from pathlib import Path

import pyray as pr

from asteroid import Asteroid
from bullet import Bullet
from config import (
    ASTEROID_COUNT,
    ASTEROID_RADIUS,
    BULLET_RADIUS,
    MAX_BULLETS,
    POINTS,
    SCREEN_H,
    SCREEN_W,
    SHIP_RADIUS,
    TITLE,
    FPS,
)
from explosion import Explosion
from ship import Ship
from utils import alive_only, circles_collide, SCREENW, SCREENH

# ── Maszyna Stanów ───────────────────────────────────────────────────────────

class State(Enum):
    MENU      = "menu"
    GAME      = "game"
    GAME_OVER = "game_over"

# ── Plik najlepszego wyniku (**) ─────────────────────────────────────────────

SCORE_FILE = Path(__file__).parent / "scores.txt"


def load_best() -> int:
    try:
        return int(SCORE_FILE.read_text().strip())
    except Exception:
        return 0


def save_best(value: int) -> None:
    try:
        SCORE_FILE.write_text(str(value))
    except Exception:
        pass

# ── Inicjalizacja okna ────────────────────────────────────────────────────────

pr.init_window(SCREEN_W, SCREEN_H, TITLE)
pr.set_target_fps(FPS)
pr.init_audio_device()

# ── Zasoby audio ──────────────────────────────────────────────────────────────

try:
    snd_shoot   = pr.load_sound("assets/shoot.wav")
    snd_explode = pr.load_sound("assets/explode.wav")
    has_audio   = True
except Exception:
    has_audio   = False

# ── Zasoby tekstury tła ───────────────────────────────────────────────────────

try:
    bg_texture  = pr.load_texture("assets/stars.png")
    has_texture = True
except Exception:
    has_texture = False
    stars = [
        (random.randint(0, SCREEN_W), random.randint(0, SCREEN_H), random.uniform(0.5, 2.0))
        for _ in range(200)
    ]

# ── Globalne zmienne gry ──────────────────────────────────────────────────────

ship:       Ship
asteroids:  list[Asteroid]
bullets:    list[Bullet]
explosions: list[Explosion]

score:    int = 0
best:     int = load_best()
wave:     int = 1
won:      bool = False       # True = zwycięstwo fali / gry

state: State = State.MENU

# ── Stałe HUD ────────────────────────────────────────────────────────────────

FONT_SIZE_BIG   = 42
FONT_SIZE_MID   = 26
FONT_SIZE_SMALL = 18

# ── Helpery ──────────────────────────────────────────────────────────────────

def _play(snd) -> None:
    if has_audio:
        pr.play_sound(snd)


def _nose_pos() -> tuple[float, float]:
    """Pozycja dzioba statku (punkt startowy pocisku)."""
    return (
        ship.pos.x + 20 * math.sin(ship.angle),
        ship.pos.y - 20 * math.cos(ship.angle),
    )


def _spawn_asteroids(count: int) -> list[Asteroid]:
    """Tworzy count asteroid poziomu 3, z dala od środka ekranu."""
    result = []
    cx, cy = SCREENW / 2, SCREENH / 2
    for _ in range(count):
        while True:
            x = random.randint(0, SCREENW)
            y = random.randint(0, SCREENH)
            if math.hypot(x - cx, y - cy) > ASTEROID_RADIUS[3] * 3:
                break
        result.append(Asteroid(x, y, level=3))
    return result

# ── init_game ─────────────────────────────────────────────────────────────────

def init_game() -> None:
    global ship, asteroids, bullets, explosions, score, wave, won
    ship       = Ship(SCREENW / 2, SCREENH / 2)
    score      = 0
    wave       = 1
    won        = False
    asteroids  = _spawn_asteroids(ASTEROID_COUNT)
    bullets    = []
    explosions = []

# ── MENU ──────────────────────────────────────────────────────────────────────

def update_menu() -> None:
    global state
    if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER) or pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
        init_game()
        state = State.GAME


def draw_menu() -> None:
    _draw_background()
    cx = SCREEN_W // 2

    title = "ASTEROIDS"
    tw = pr.measure_text(title, FONT_SIZE_BIG)
    pr.draw_text(title, cx - tw // 2, 180, FONT_SIZE_BIG, pr.WHITE)

    sub = "Nacisnij SPACJE lub ENTER aby rozpoczac"
    sw = pr.measure_text(sub, FONT_SIZE_SMALL)
    pr.draw_text(sub, cx - sw // 2, 260, FONT_SIZE_SMALL, pr.GRAY)

    best_txt = f"Najlepszy wynik sesji: {best}"
    bw = pr.measure_text(best_txt, FONT_SIZE_SMALL)
    pr.draw_text(best_txt, cx - bw // 2, 320, FONT_SIZE_SMALL, pr.GOLD)

    ctrl = "[UP] silnik  [LEFT/RIGHT] obrot  [SPACE] strzal  [Z] hamulec"
    cw = pr.measure_text(ctrl, 14)
    pr.draw_text(ctrl, cx - cw // 2, SCREEN_H - 40, 14, pr.DARKGRAY)

# ── GAME ──────────────────────────────────────────────────────────────────────

def update_game(dt: float) -> None:
    global state, score, best, wave, won, asteroids, bullets, explosions

    ship.update(dt)

    # strzelanie
    if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE) and len(bullets) < MAX_BULLETS:
        nx, ny = _nose_pos()
        bullets.append(Bullet(nx, ny, ship.angle))
        _play(snd_shoot)

    for b in bullets:
        b.update(dt)
    for a in asteroids:
        a.update(dt)
    for e in explosions:
        e.update(dt)

    # kolizje pocisków z asteroidami
    new_asteroids: list[Asteroid] = []
    for b in bullets:
        if not b.alive:
            continue
        for a in asteroids:
            if not a.alive:
                continue
            if circles_collide(b.x, b.y, BULLET_RADIUS, a.pos.x, a.pos.y, a.radius):
                b.alive = False
                a.alive = False
                score  += POINTS[a.level]
                explosions.append(Explosion(a.pos.x, a.pos.y, a.radius * 1.5))
                _play(snd_explode)
                new_asteroids.extend(a.split())   # Zadanie 1: podział

    asteroids.extend(new_asteroids)

    # czyszczenie list
    bullets    = alive_only(bullets)
    asteroids  = alive_only(asteroids)
    explosions = alive_only(explosions)

    # ── Warunek zwycięstwa (Zadanie 5) ───────────────────────────────────────
    if not asteroids:
        # nowa fala (*) – gra trwa dalej
        wave += 1
        asteroids = _spawn_asteroids(ASTEROID_COUNT + wave - 1)
        # (opcjonalnie można tu dać krótką przerwę przez timer w draw)

    # ── Kolizja statku z asteroidą (Zadanie 5) ─────────────────────────────
    for a in asteroids:
        if circles_collide(ship.pos.x, ship.pos.y, SHIP_RADIUS, a.pos.x, a.pos.y, a.radius):
            a.alive = False
            explosions.append(Explosion(ship.pos.x, ship.pos.y, 40.0))
            _play(snd_explode)
            # aktualizacja best przed przejściem
            if score > best:
                best = score
                save_best(best)
            state = State.GAME_OVER
            won   = False
            return

    asteroids = alive_only(asteroids)


def draw_game() -> None:
    _draw_background()
    for a in asteroids:
        a.draw()
    for b in bullets:
        b.draw()
    for e in explosions:
        e.draw()
    ship.draw()
    draw_hud()


def draw_hud() -> None:
    """HUD: wynik, najlepszy wynik, fala, liczba pocisków."""
    pr.draw_text(f"Wynik: {score}", 10, 10, FONT_SIZE_SMALL, pr.GREEN)
    pr.draw_text(f"Best:  {best}",  10, 32, FONT_SIZE_SMALL, pr.GOLD)
    pr.draw_text(f"Fala:  {wave}",  10, 54, FONT_SIZE_SMALL, pr.SKYBLUE)

    bullet_txt = f"Pociski: {len(bullets)}/{MAX_BULLETS}"
    bw = pr.measure_text(bullet_txt, FONT_SIZE_SMALL)
    pr.draw_text(bullet_txt, SCREEN_W - bw - 10, 10, FONT_SIZE_SMALL, pr.RAYWHITE)

    asteroid_txt = f"Asteroidy: {len(asteroids)}"
    aw = pr.measure_text(asteroid_txt, FONT_SIZE_SMALL)
    pr.draw_text(asteroid_txt, SCREEN_W - aw - 10, 32, FONT_SIZE_SMALL, pr.RAYWHITE)

# ── GAME_OVER ─────────────────────────────────────────────────────────────────

def update_game_over() -> None:
    global state, best
    if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER) or pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
        if score > best:
            best = score
            save_best(best)
        state = State.MENU


def draw_game_over() -> None:
    _draw_background()
    # dokonczmy rysowanie eksplozji jesli jeszcze trwa
    for e in explosions:
        e.draw()

    cx = SCREEN_W // 2

    header = "ZWYCIESTWO!" if won else "GAME OVER"
    color  = pr.GREEN if won else pr.RED
    hw = pr.measure_text(header, FONT_SIZE_BIG)
    pr.draw_text(header, cx - hw // 2, 170, FONT_SIZE_BIG, color)

    score_txt = f"Wynik: {score}"
    sw = pr.measure_text(score_txt, FONT_SIZE_MID)
    pr.draw_text(score_txt, cx - sw // 2, 240, FONT_SIZE_MID, pr.WHITE)

    best_txt = f"Najlepszy wynik sesji: {best}"
    bw = pr.measure_text(best_txt, FONT_SIZE_SMALL)
    pr.draw_text(best_txt, cx - bw // 2, 285, FONT_SIZE_SMALL, pr.GOLD)

    new_record = score >= best and score > 0
    if new_record:
        rec_txt = "NOWY REKORD!"
        rw = pr.measure_text(rec_txt, FONT_SIZE_SMALL)
        pr.draw_text(rec_txt, cx - rw // 2, 315, FONT_SIZE_SMALL, pr.YELLOW)

    restart_txt = "Nacisnij SPACJE lub ENTER – powrot do menu"
    rw2 = pr.measure_text(restart_txt, FONT_SIZE_SMALL)
    pr.draw_text(restart_txt, cx - rw2 // 2, SCREEN_H - 60, FONT_SIZE_SMALL, pr.GRAY)

# ── Tło ───────────────────────────────────────────────────────────────────────

def _draw_background() -> None:
    pr.clear_background(pr.BLACK)
    if has_texture:
        pr.draw_texture(bg_texture, 0, 0, pr.WHITE)
    else:
        for sx, sy, sr in stars:
            pr.draw_circle(int(sx), int(sy), sr, pr.RAYWHITE)

# ── Pętla główna ──────────────────────────────────────────────────────────────

while not pr.window_should_close():
    dt = pr.get_frame_time()

    # ── update ────────────────────────────────────────────────────────────────
    if state is State.MENU:
        update_menu()
    elif state is State.GAME:
        update_game(dt)
    elif state is State.GAME_OVER:
        update_game_over()

    # ── draw ──────────────────────────────────────────────────────────────────
    pr.begin_drawing()
    if state is State.MENU:
        draw_menu()
    elif state is State.GAME:
        draw_game()
    elif state is State.GAME_OVER:
        draw_game_over()
    pr.end_drawing()

# ── Zwalnianie zasobów ────────────────────────────────────────────────────────

if has_audio:
    pr.unload_sound(snd_shoot)
    pr.unload_sound(snd_explode)
    pr.close_audio_device()

if has_texture:
    pr.unload_texture(bg_texture)

pr.close_window()