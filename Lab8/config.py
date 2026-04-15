# ── ekran ──────────────────────────────────────────────────────────────────
SCREEN_W: int   = 800
SCREEN_H: int   = 600
FPS:      int   = 60
TITLE:    str   = "Asteroids – Lab 08"

# ── statek ─────────────────────────────────────────────────────────────────
THRUST:    float = 220.0   # przyspieszenie
FRICTION:  float = 60.0    # tarcie
ROTSPEED:  float = 3.2     # predkosc obrotu [rad/s]
MAXSPEED:  float = 350.0   # ograniczenie predkosci
SHIP_SIZE: float = 16.0    # przyblizony promien statku
SHIP_RADIUS: float = 15.0  # promien kolizji statku

# ── pociski ─────────────────────────────────────────────────────────────────
BULLET_SPEED:  float = 500.0
BULLET_TTL:    float = 2.0
BULLET_RADIUS: int   = 4
MAX_BULLETS:   int   = 5

# ── asteroidy ──────────────────────────────────────────────────────────────
ASTEROID_COUNT:   int   = 6     # liczba wielkich asteroid na starcie
ASTEROID_JITTER:  float = 0.35  # max odchylenie promienia wierzcholkow
ASTEROID_SPEED_K: float = 90.0  # predkosc bazowa  (v = K / radius)
ASTEROID_ROT_MAX: float = 1.8   # max predkosc katowa [rad/s]

# promienie (radius) na kazdy poziom
ASTEROID_RADIUS: dict[int, float] = {
    3: 52.0,   # poziom 3 – wielka
    2: 30.0,   # poziom 2 – srednia
    1: 14.0,   # poziom 1 – mala
}

# liczba wierzcholkow wielokata na kazdy poziom
ASTEROID_VERTS: dict[int, int] = {
    3: 11,
    2: 8,
    1: 6,
}

# punkty za zniszczenie asteroidy danego poziomu
POINTS: dict[int, int] = {
    3: 20,
    2: 50,
    1: 100,
}

# ── debug ──────────────────────────────────────────────────────────────────
DEBUG: bool = False
