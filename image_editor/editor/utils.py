def validate_coordinates(coords, max_width, max_height):
    """Проверяет корректность координат"""
    if len(coords) != 4:
        return False
    x1, y1, x2, y2 = coords
    return (0 <= x1 < x2 <= max_width and
            0 <= y1 < y2 <= max_height)