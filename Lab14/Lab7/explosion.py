import pyray as pr

EXPLOSION_DURATION = 0.5  # czas trwania wybuchu


class Explosion:
    def __init__(self, x: float, y: float, max_radius: float = 40.0):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.timer = 0.0
        self.alive = True

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= EXPLOSION_DURATION:
            self.alive = False

    def draw(self):
        progress = self.timer / EXPLOSION_DURATION          # postep wybuchu
        radius = self.max_radius * progress
        # zanikanie i zmiana koloru
        alpha = int(255 * (1.0 - progress))
        color = pr.Color(255, int(165 * (1.0 - progress) + 90), 0, alpha)
        pr.draw_circle_lines(int(self.x), int(self.y), max(1, radius), color)
        # wewnetrzne kolo
        inner = radius * 0.5
        pr.draw_circle_lines(int(self.x), int(self.y), max(1, inner),
                             pr.Color(255, 255, 200, alpha))