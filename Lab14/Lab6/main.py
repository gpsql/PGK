import random
import pyray as rl

from utils import SCREENW, SCREENH
from config import ASTEROID_COUNT
from ship import Ship
from asteroid import Asteroid, Size

TARGET_FPS = 60

_SIZE_POOL = [Size.LARGE, Size.LARGE, Size.MEDIUM, Size.MEDIUM, Size.SMALL, Size.SMALL]


def _spawn_asteroids(count: int, ship_x: float, ship_y: float) -> list[Asteroid]:
    MIN_DIST = 120.0
    sizes = (_SIZE_POOL * ((count // len(_SIZE_POOL)) + 1))[:count]
    random.shuffle(sizes)
    asteroids: list[Asteroid] = []
    for size in sizes:
        while True:
            x = random.uniform(0, SCREENW)
            y = random.uniform(0, SCREENH)
            if abs(x - ship_x) > MIN_DIST or abs(y - ship_y) > MIN_DIST:
                break
        asteroids.append(Asteroid(x, y, size))
    return asteroids


def main() -> None:
    rl.init_window(SCREENW, SCREENH, "Lab 06 – Asteroidy (torus + ghost rendering)")
    rl.set_target_fps(TARGET_FPS)

    ship = Ship(SCREENW / 2, SCREENH / 2)
    asteroids = _spawn_asteroids(ASTEROID_COUNT, SCREENW / 2, SCREENH / 2)

    while not rl.window_should_close():
        dt = rl.get_frame_time()
        ship.update(dt)
        ship.wrap()

        for asteroid in asteroids:
            asteroid.update(dt)
            asteroid.wrap()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        for asteroid in asteroids:
            asteroid.draw()

        ship.draw()

        rl.draw_text(
            "Strzalki: obrot + ciag  |  Z: hamulec awaryjny",
            10, 10, 14, rl.DARKGRAY,
        )
        rl.draw_fps(SCREENW - 80, 10)

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()