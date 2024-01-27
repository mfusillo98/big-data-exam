from math import radians, degrees, sin, cos, sqrt, atan2


# add kilometers to lat and long
def sum_km_to_coordinates(lat, long, km):
    # Earth radius in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude to radians
    lat_radians = radians(lat)
    lon_radians = radians(long)

    # Calculate the new latitude using Haversine formula
    new_lat_radians = lat_radians + (km / earth_radius)

    # Calculate the new longitude using Haversine formula
    new_lon_radians = lon_radians + (km / (earth_radius * cos(lat_radians)))

    # Convert the new latitude and longitude back to degrees
    new_latitude = degrees(new_lat_radians)
    new_longitude = degrees(new_lon_radians)

    return new_latitude, new_longitude