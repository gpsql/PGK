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