import math

import pyray as rl

from config import THRUST, FRICTION, ROTSPEED, MAXSPEED, SHIP_SIZE, DEBUG
from utils import SCREENW, SCREENH, ghost_positions


#wierzcholki statku w ukladzie lokalnym (dziób skierowany w gore = -y)
_SHIP_VERTS: list[tuple[float, float]] = [
    (  0.0, -16.0),   # dziób
    (-11.0,  12.0),   # lewe skrzydło
    (  0.0,   7.0),   # tylne wcięcie
    ( 11.0,  12.0),   # prawe skrzydło
]

_FLAME_VERTS: list[tuple[float, float]] = [
    (-6.0,  10.0),
    ( 6.0,  10.0),
    ( 0.0,  26.0),
]

_FLAME_INNER: list[tuple[float, float]] = [
    (-3.5, 11.0),
    ( 3.5, 11.0),
    ( 0.0, 20.0),
]


def _rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    """Obrót punktu (x,y) wokół (0,0) o kąt angle [rad]."""
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


def _world_verts(
    local_verts: list[tuple[float, float]],
    angle: float,
    ox: float,
    oy: float,
) -> list[rl.Vector2]:
    return [
        rl.Vector2(ox + rx, oy + ry)
        for lx, ly in local_verts
        for rx, ry in [_rotate(lx, ly, angle)]
    ]


class Ship:
    def __init__(self, x: float, y: float) -> None:
        self.pos        = rl.Vector2(x, y)
        self.angle      = 0.0
        self.vel        = rl.Vector2(0.0, 0.0)
        self._thrusting = False

    #publiczne API 
    def update(self, dt: float) -> None:
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.angle -= ROTSPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.angle += ROTSPEED * dt

        #kierunek dzioba
        nose_x =  math.sin(self.angle)
        nose_y = -math.cos(self.angle)

        self._thrusting = rl.is_key_down(rl.KeyboardKey.KEY_UP)
        if self._thrusting:
            self.vel.x += nose_x * THRUST * dt
            self.vel.y += nose_y * THRUST * dt

        #tarcie (z= hamulec ręczny)
        friction_multiplier = 8.0 if rl.is_key_down(rl.KeyboardKey.KEY_Z) else 1.0
        self._apply_friction(FRICTION * friction_multiplier * dt)

        # Limit prędkości
        speed = math.hypot(self.vel.x, self.vel.y)
        if speed > MAXSPEED:
            scale = MAXSPEED / speed
            self.vel.x *= scale
            self.vel.y *= scale

        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

    def wrap(self) -> None:
        self.pos.x = self.pos.x % SCREENW
        self.pos.y = self.pos.y % SCREENH

    def draw(self) -> None:
        for px, py in ghost_positions(self.pos.x, self.pos.y, SHIP_SIZE):
            self._draw_at(px, py)

    #prywatne 
    def _apply_friction(self, delta: float) -> None:
        speed = math.hypot(self.vel.x, self.vel.y)
        if speed < 1e-4:
            self.vel.x = self.vel.y = 0.0
            return
        factor = max(0.0, speed - delta) / speed
        self.vel.x *= factor
        self.vel.y *= factor

    def _draw_at(self, ox: float, oy: float) -> None:
        if self._thrusting:
            flame_verts = _world_verts(_FLAME_VERTS, self.angle, ox, oy)
            rl.draw_triangle_lines(flame_verts[0], flame_verts[1], flame_verts[2], rl.ORANGE)
            inner_verts = _world_verts(_FLAME_INNER, self.angle, ox, oy)
            rl.draw_triangle(inner_verts[0], inner_verts[1], inner_verts[2], rl.YELLOW)

        ship_verts = _world_verts(_SHIP_VERTS, self.angle, ox, oy)
        n = len(ship_verts)
        for i in range(n):
            rl.draw_line_v(ship_verts[i], ship_verts[(i + 1) % n], rl.WHITE)

        if DEBUG:
            speed  = math.hypot(self.vel.x, self.vel.y)
            tip_x  = ox + self.vel.x * 0.4
            tip_y  = oy + self.vel.y * 0.4
            rl.draw_line_v(rl.Vector2(ox, oy), rl.Vector2(tip_x, tip_y), rl.GREEN)
            rl.draw_circle_v(rl.Vector2(tip_x, tip_y), 3, rl.GREEN)
            rl.draw_text(f"spd:{speed:.0f}", int(ox) + 14, int(oy) - 8, 12, rl.LIME)