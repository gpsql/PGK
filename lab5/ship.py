import math
import pyray as rl

from config import THRUST, FRICTION, ROTSPEED, MAXSPEED, SHIP_SIZE, DEBUG
from utils import SCREENW, SCREENH, ghost_positions

#geometria statku 
VERTS = [
    ( 0.0, -16.0),   # dziob
    (-11.0,  12.0),  # lewe skrzydlo
    (  0.0,   7.0),  # tylne wciecie
    ( 11.0,  12.0),  # prawe skrzydlo
]

FLAME_VERTS = [
    (-6.0,  10.0),
    ( 6.0,  10.0),
    ( 0.0,  26.0),
]

#matematyka
def _rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    """Obrót punktu (x, y) wokół (0,0) o kąt angle [rad].

        x' = x·cos α − y·sin α
        y' = x·sin α + y·cos α

    W Raylib oś Y rośnie w dół, więc wzór działa bez modyfikacji.
    """
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

    #publiczne api
    def update(self, dt: float) -> None:
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.angle -= ROTSPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.angle += ROTSPEED * dt

        nx =  math.sin(self.angle)
        ny = -math.cos(self.angle)

        self._thrusting = rl.is_key_down(rl.KeyboardKey.KEY_UP)
        if self._thrusting:
            self.vel.x += nx * THRUST * dt
            self.vel.y += ny * THRUST * dt

        friction_dt = FRICTION * (8.0 if rl.is_key_down(rl.KeyboardKey.KEY_Z) else 1.0) * dt
        self._apply_friction(friction_dt)

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
            fw = _world_verts(FLAME_VERTS, self.angle, ox, oy)
            rl.draw_triangle_lines(fw[0], fw[1], fw[2], rl.ORANGE)
            inner = [(-3.5, 11.0), (3.5, 11.0), (0.0, 20.0)]
            iw = _world_verts(inner, self.angle, ox, oy)
            rl.draw_triangle(iw[0], iw[1], iw[2], rl.YELLOW)

        wv = _world_verts(VERTS, self.angle, ox, oy)
        n = len(wv)
        for i in range(n):
            rl.draw_line_v(wv[i], wv[(i + 1) % n], rl.WHITE)

        if DEBUG:
            speed = math.hypot(self.vel.x, self.vel.y)
            ex = ox + self.vel.x * 0.4
            ey = oy + self.vel.y * 0.4
            rl.draw_line_v(rl.Vector2(ox, oy), rl.Vector2(ex, ey), rl.GREEN)
            rl.draw_circle_v(rl.Vector2(ex, ey), 3, rl.GREEN)
            rl.draw_text(f"spd:{speed:.0f}", int(ox) + 14, int(oy) - 8, 12, rl.LIME)