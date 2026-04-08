import math

SCREENW: int = 800
SCREENH: int = 600

def ghost_positions(x: float, y: float, size: float) -> list[tuple[float, float]]:
    xs: list[float] = [x]
    ys: list[float] = [y]

    if x < size:
        xs.append(x + SCREENW)
    elif x > SCREENW - size:
        xs.append(x - SCREENW)

    if y < size:
        ys.append(y + SCREENH)
    elif y > SCREENH - size:
        ys.append(y - SCREENH)

    return [(px, py) for px in xs for py in ys]


def circles_collide(x1: float, y1: float, r1: float,
                    x2: float, y2: float, r2: float) -> bool:
    """Zwraca True jesli okregi wpadaja na siebie"""
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance < r1 + r2