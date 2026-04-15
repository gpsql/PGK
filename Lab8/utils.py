import math
from typing import TypeVar

SCREENW: int = 800
SCREENH: int = 600

_T = TypeVar("_T")

def ghost_positions(x: float, y: float, size: float) -> list[tuple[float, float]]:
    """zwraca liste pozycji 'widmowych' do rysowania przy krawedziach ekranu"""
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

def circles_collide(
    x1: float, y1: float, r1: float,
    x2: float, y2: float, r2: float,
) -> bool:
    """zwraca true jesli dwa okregi nachodza na siebie"""
    return math.hypot(x2 - x1, y2 - y1) < r1 + r2

def alive_only(objects: list[_T]) -> list[_T]:
    return [obj for obj in objects if obj.alive]  