import math
def haversine(latitude1, longitude1, latitude2, longitude2):
    RAYON_TERRRE = 6371  # Rayon de la Terre en km
    delta_latitude = math.radians(latitude2 - latitude1)
    delta_longitude = math.radians(longitude2 - longitude1)
    a = math.sin(delta_latitude / 2) ** 2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(delta_longitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return RAYON_TERRRE * c  # Retourne la distance en km