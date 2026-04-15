import pyray as pr

from config import EXPLOSION_DURATION


class Explosion:
    def __init__(self, x: float, y: float, max_radius: float = 40.0) -> None:
        self.x          = x
        self.y          = y
        self.max_radius = max_radius
        self.timer      = 0.0
        self.alive      = True

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= EXPLOSION_DURATION:
            self.alive = False

    def draw(self) -> None:
        progress = self.timer / EXPLOSION_DURATION
        radius   = self.max_radius * progress
        alpha    = int(255 * (1.0 - progress))

        outer_color = pr.Color(255, int(165 * (1.0 - progress) + 90), 0, alpha)
        inner_color = pr.Color(255, 255, 200, alpha)

        pr.draw_circle_lines(int(self.x), int(self.y), max(1.0, radius), outer_color)
        pr.draw_circle_lines(int(self.x), int(self.y), max(1.0, radius * 0.5), inner_color)