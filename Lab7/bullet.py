import math
import pyray as pr

BULLET_SPEED = 500
BULLET_TTL = 2.0      # max czas zycia pocisku
BULLET_RADIUS = 4
SCREEN_W = 800
SCREEN_H = 600


class Bullet:
    def __init__(self, x: float, y: float, angle_rad: float):
        self.x = x
        self.y = y
        self.vx = math.sin(angle_rad) * BULLET_SPEED
        self.vy = -math.cos(angle_rad) * BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL
        self.alive = True

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False  # ginie po czasie
        # zawijanie krawedzi
        self.x %= SCREEN_W
        self.y %= SCREEN_H

    def draw(self):
        pr.draw_circle(int(self.x), int(self.y), self.radius, pr.YELLOW)