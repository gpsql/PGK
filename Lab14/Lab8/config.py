#okno
SCREEN_TITLE: str  = "Asteroids – Lab 08"
TITLE:        str  = SCREEN_TITLE       # alias uzywany w main.py
SCREEN_W:     int  = 800
SCREEN_H:     int  = 600
FPS:          int  = 60

#statek
THRUST:    float = 220.0   # przyspieszenie [px/s²]
FRICTION:  float =  60.0   # tarcie [px/s²]
ROTSPEED:  float =   3.2   # predkosc obrotu [rad/s]
MAXSPEED:  float = 350.0   # limit predkosci [px/s]
SHIP_SIZE:   float = 16.0  # rozmiar graficzny statku [px]
SHIP_RADIUS: float = 14.0  # promien kolizji statku [px]
SHIP_NOSE_OFFSET: float = 20.0  # odleglosc lufy od srodka [px]

#pociski
BULLET_SPEED:  int   = 500
BULLET_TTL:    float =   2.0
BULLET_RADIUS: int   =   4
MAX_BULLETS:   int   =   5

#asteroidy- wspolne
ASTEROID_COUNT:   int   =  6
ASTEROID_JITTER:  float =  0.35
ASTEROID_SPEED_K: float = 90.0   # predkosc bazowa (dzielona przez promień)
ASTEROID_ROT_MAX: float =  1.8   # max predkosc kątowa [rad/s]

# Parametry per poziom (3 = duża, 2 = średnia, 1 = mała)
ASTEROID_RADIUS: dict[int, float] = {3: 52.0, 2: 30.0, 1: 14.0}
ASTEROID_VERTS:  dict[int, int]   = {3: 11,   2:  8,   1:  6}

# Punkty za zniszczenie asteroidy danego poziomu
# (mniejsza asteroida = trudniejsza do trafienia = więcej punktów)
POINTS: dict[int, int] = {3: 20, 2: 50, 1: 100}

# Eksplozja
EXPLOSION_DURATION: float = 0.5

# Debug
DEBUG: bool = False