import math
import pyray as rl

THRUST    = 220.0   
FRICTION  = 60.0   
ROTSPEED  = 3.2     
MAXSPEED  = 350.0   
DEBUG = False

VERTS = [
    ( 0.0, -16.0), 
    (-11.0,  12.0),  
    (  0.0,   7.0),  
    ( 11.0,  12.0), 
]

FLAME_VERTS = [
    (-6.0,  10.0),   
    ( 6.0,  10.0), 
    ( 0.0,  26.0),   
]


def _rotate(x: float, y: float, angle: float) -> tuple[float, float]:
    """Obrót punktu (x, y) wokół (0,0) o kąt angle [rad].

    Macierz 2D:
        x' =  x·cos(α) − y·sin(α)
        y' =  x·sin(α) + y·cos(α)

    W Raylib oś Y rośnie w dół, więc wzór działa bez zmian –
    kąt dodatni = obrót zgodnie z ruchem wskazówek zegara.
    """
    c = math.cos(angle)
    s = math.sin(angle)
    return x * c - y * s, x * s + y * c


def _world_verts(local_verts, angle: float, ox: float, oy: float) -> list[rl.Vector2]:
    """Przekształca listę lokalnych wierzchołków na współrzędne ekranu."""
    result = []
    for lx, ly in local_verts:
        rx, ry = _rotate(lx, ly, angle)
        result.append(rl.Vector2(ox + rx, oy + ry))
    return result


class Ship:
    def __init__(self, x: float, y: float):
        self.pos   = rl.Vector2(x, y)
        self.angle = 0.0         
        self.vel   = rl.Vector2(0.0, 0.0)
        self._thrusting = False  

    def update(self, dt: float) -> None:
        """Fizyka niezależna od FPS – każda wielkość mnożona przez dt."""

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

        if rl.is_key_down(rl.KeyboardKey.KEY_Z):
            self._apply_friction(FRICTION * 8.0 * dt)
        else:
            self._apply_friction(FRICTION * dt)

        speed = math.hypot(self.vel.x, self.vel.y)
        if speed > MAXSPEED:
            scale = MAXSPEED / speed
            self.vel.x *= scale
            self.vel.y *= scale

        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

        sw = rl.get_screen_width()
        sh = rl.get_screen_height()
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = abs(self.vel.x)
        elif self.pos.x > sw:
            self.pos.x = float(sw)
            self.vel.x = -abs(self.vel.x)
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = abs(self.vel.y)
        elif self.pos.y > sh:
            self.pos.y = float(sh)
            self.vel.y = -abs(self.vel.y)

    def _apply_friction(self, delta: float) -> None:
        """Tarcie addytywne: zmniejsza prędkość o delta, nie przeskakuje przez 0."""
        speed = math.hypot(self.vel.x, self.vel.y)
        if speed < 1e-4:
            self.vel.x = 0.0
            self.vel.y = 0.0
            return

        factor = max(0.0, speed - delta) / speed
        self.vel.x *= factor
        self.vel.y *= factor

    def draw(self) -> None:
        ox, oy = self.pos.x, self.pos.y

        if self._thrusting:
            fw = _world_verts(FLAME_VERTS, self.angle, ox, oy)
            rl.draw_triangle_lines(fw[0], fw[1], fw[2], rl.ORANGE)
            inner = [
                (-3.5, 11.0),
                ( 3.5, 11.0),
                ( 0.0, 20.0),
            ]
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
            rl.draw_text(
                f"spd: {speed:.1f} px/s",
                int(ox) + 14, int(oy) - 8,
                14, rl.LIME
            )