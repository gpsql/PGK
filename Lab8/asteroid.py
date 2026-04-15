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


def _rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


# kolory per poziom
_LEVEL_COLOR = {
    3: rl.GRAY,
    2: rl.LIGHTGRAY,
    1: rl.WHITE,
}


class Asteroid:
    """Asteroida z trzema poziomami (3=wielka, 2=srednia, 1=mala)."""

    def __init__(self, x: float, y: float, level: int = 3) -> None:
        self.pos   = rl.Vector2(x, y)
        self.level = level
        self.alive = True

        self.radius    = ASTEROID_RADIUS[level]
        self._color    = _LEVEL_COLOR[level]
        n_verts        = ASTEROID_VERTS[level]

        speed = ASTEROID_SPEED_K / self.radius
        angle = random.uniform(0.0, math.tau)
        self.vel = rl.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed,
        )

        self.angle     = random.uniform(0.0, math.tau)
        self.rot_speed = random.uniform(-ASTEROID_ROT_MAX, ASTEROID_ROT_MAX)

        # generujemy nieregularny wielokat lokalnie
        self._local_verts: list[tuple[float, float]] = []
        for i in range(n_verts):
            theta = (math.tau / n_verts) * i
            r = self.radius * random.uniform(1.0 - ASTEROID_JITTER, 1.0 + ASTEROID_JITTER)
            self._local_verts.append((math.cos(theta) * r, math.sin(theta) * r))

    # ── logika ───────────────────────────────────────────────────────────────

    def update(self, dt: float) -> None:
        self.pos.x  += self.vel.x * dt
        self.pos.y  += self.vel.y * dt
        self.angle  += self.rot_speed * dt
        self.pos.x  %= SCREENW
        self.pos.y  %= SCREENH

    def split(self) -> list["Asteroid"]:
        """Zwraca dwie mniejsze asteroidy lub [] gdy level == 1."""
        if self.level == 1:
            return []
        children = []
        for _ in range(2):
            child = Asteroid(self.pos.x, self.pos.y, self.level - 1)
            # losowy kierunek rozproszenia
            spread_angle = random.uniform(0.0, math.tau)
            extra_speed  = ASTEROID_SPEED_K / child.radius * 0.5
            child.vel.x += math.cos(spread_angle) * extra_speed
            child.vel.y += math.sin(spread_angle) * extra_speed
            children.append(child)
        return children

    # ── rysowanie ────────────────────────────────────────────────────────────

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