import math
import random
from enum import Enum, auto

import pyray as rl

from config import (
    ASTEROID_JITTER,
    ASTEROID_SPEED_K,
    ASTEROID_ROT_MAX,
)
from utils import SCREENW, SCREENH, ghost_positions


def _rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


class Size(Enum):
    LARGE  = auto()
    MEDIUM = auto()
    SMALL  = auto()


_SIZE_PARAMS: dict[Size, tuple[float, int, object]] = {
    Size.LARGE:  (52.0,  11, rl.GRAY),
    Size.MEDIUM: (30.0,   8, rl.LIGHTGRAY),
    Size.SMALL:  (14.0,   6, rl.WHITE),
}


class Asteroid:
    def __init__(self, x: float, y: float, size: Size = Size.LARGE) -> None:
        self.pos  = rl.Vector2(x, y)
        self.size = size

        radius, n_verts, self._color = _SIZE_PARAMS[size]
        self.radius = radius

        speed = ASTEROID_SPEED_K / radius
        angle = random.uniform(0.0, math.tau)   # math.tau = 2π
        self.vel = rl.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed,
        )

        self.angle     = random.uniform(0.0, math.tau)
        self.rot_speed = random.uniform(-ASTEROID_ROT_MAX, ASTEROID_ROT_MAX)

        self._local_verts: list[tuple[float, float]] = []
        for i in range(n_verts):
            theta = (math.tau / n_verts) * i
            r = radius * random.uniform(1.0 - ASTEROID_JITTER, 1.0 + ASTEROID_JITTER)
            self._local_verts.append((math.cos(theta) * r, math.sin(theta) * r))

    def update(self, dt: float) -> None:
        self.pos.x   += self.vel.x   * dt
        self.pos.y   += self.vel.y   * dt
        self.angle   += self.rot_speed * dt

    def wrap(self) -> None:
        self.pos.x = self.pos.x % SCREENW
        self.pos.y = self.pos.y % SCREENH

    def draw(self) -> None:
        """Rysuje wielokąt (z rotacją) dla każdej pozycji widmowej."""
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