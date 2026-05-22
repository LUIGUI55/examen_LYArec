from math import sin, cos, acos

def geo_dist(lat1, lon1, lat2, lon2):
    grad_rad = 0.0174539
    rad_grad = 57.29577951
    longitud = lon1 - lon2
    val = (sin(lat1 * grad_rad) * sin(lat2 * grad_rad)) + (cos(lat1 * grad_rad) * cos(lat2 * grad_rad) * cos(longitud * grad_rad))
    # Evitar errores fuera del rango de acos por precisión decimal
    val = max(-1.0, min(1.0, val))
    return (acos(val) * rad_grad) * 111.32