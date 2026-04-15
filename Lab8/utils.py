import math
from config import SCREEN_W, SCREEN_H

SCREENW: int = SCREEN_W
SCREENH: int = SCREEN_H


def ghost_positions(x: float, y: float, size: float) -> list[tuple[float, float]]:
    """Zwraca liste pozycji do rysowania obiektu z efektem widmo na krawedziach."""
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
    """Zwraca True jesli okregi wpadaja na siebie."""
    return math.hypot(x2 - x1, y2 - y1) < r1 + r2


def alive_only(objects: list) -> list:
    """Zwraca liste obiektow, ktore maja alive == True."""
    return [obj for obj in objects if obj.alive]