import math
import random

import pyray as rl

from config import (
    ASTEROID_JITTER,
    ASTEROID_SPEED_K,
    ASTEROID_ROT_MAX,
    ASTEROID_RADIUS,
    ASTEROID_VERTS,
)
from utils import SCREENW, SCREENH, ghost_positions


#kolory wizualnie sugeruja rozmiar asteroidy
_LEVEL_COLOR: dict[int, object] = {
    3: rl.GRAY,
    2: rl.LIGHTGRAY,
    1: rl.WHITE,
}


def _rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


class Asteroid:
    def __init__(self, x: float, y: float, level: int = 3) -> None:
        """
        level=3  duza, wolna
        level=2  srednia
        level=1  mala, szybka
        """
        self.pos   = rl.Vector2(x, y)
        self.level = level
        self.alive = True

        self.radius = ASTEROID_RADIUS[level]
        self._color = _LEVEL_COLOR[level]
        n_verts     = ASTEROID_VERTS[level]

        #mniejszy promien -> wiekszy iloraz -> wyzsza predkosc
        speed = ASTEROID_SPEED_K / self.radius
        angle = random.uniform(0.0, math.tau)   # math.tau == 2π
        self.vel = rl.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed,
        )

        self.angle     = random.uniform(0.0, math.tau)
        self.rot_speed = random.uniform(-ASTEROID_ROT_MAX, ASTEROID_ROT_MAX)

        #generowanie nieregularnego wielokata w ukladzie lokalnym
        self._local_verts: list[tuple[float, float]] = []
        for i in range(n_verts):
            theta = (math.tau / n_verts) * i
            r = self.radius * random.uniform(
                1.0 - ASTEROID_JITTER,
                1.0 + ASTEROID_JITTER,
            )
            self._local_verts.append((math.cos(theta) * r, math.sin(theta) * r))

    #logika 
    def update(self, dt: float) -> None:
        self.pos.x  += self.vel.x   * dt
        self.pos.y  += self.vel.y   * dt
        self.angle  += self.rot_speed * dt

    def wrap(self) -> None:
        self.pos.x = self.pos.x % SCREENW
        self.pos.y = self.pos.y % SCREENH

    def split(self) -> list["Asteroid"]:
        """Zwraca dwie mniejsze asteroidy lub pustą listę (poziom 1).

        ZADANIE 1 – enkapsulacja: to asteroida wie, jak się podzielić.
        main.py tylko wywołuje split() i dodaje wynik do listy.
        """
        if self.level == 1:
            return []
        return [
            Asteroid(self.pos.x, self.pos.y, self.level - 1),
            Asteroid(self.pos.x, self.pos.y, self.level - 1),
        ]

    #rysowanie 
    def draw(self) -> None:
        for px, py in ghost_positions(self.pos.x, self.pos.y, self.radius):
            self._draw_at(px, py)

    def _draw_at(self, ox: float, oy: float) -> None:
        world: list[rl.Vector2] = []
        for lx, ly in self._local_verts:
            rx, ry = _rotate(lx, ly, self.angle)
            world.append(rl.Vector2(ox + rx, oy + ry))

        n = len(world)
        for i in range(n):
            rl.draw_line_v(world[i], world[(i + 1) % n], self._color)