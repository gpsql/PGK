import math

import pyray as pr

from config import BULLET_SPEED, BULLET_TTL, BULLET_RADIUS
from utils import SCREENW, SCREENH


class Bullet:
    def __init__(self, x: float, y: float, angle_rad: float) -> None:
        self.x  = x
        self.y  = y
        self.vx = math.sin(angle_rad) * BULLET_SPEED
        self.vy = -math.cos(angle_rad) * BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.ttl    = BULLET_TTL
        self.alive  = True

    def update(self, dt: float) -> None:
        self.x   += self.vx * dt
        self.y   += self.vy * dt
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False
        self.x %= SCREENW
        self.y %= SCREENH

    def draw(self) -> None:
        pr.draw_circle(int(self.x), int(self.y), self.radius, pr.YELLOW)