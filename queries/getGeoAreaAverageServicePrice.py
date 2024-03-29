from app.database.database import get_db
from app.utils.geolocationUtils import sum_km_to_coordinates


'''
1 Prezzo medio di un servizio in un area geolocalizzata
'''

def get_geo_area_average_service_price(service, lat, long, km_radius):
    db = get_db()

    max_lat, max_long = sum_km_to_coordinates(lat, long, km_radius)
    min_lat, min_long = sum_km_to_coordinates(lat, long, -km_radius)

    query = "SELECT AVG(b.price) as avg_price " \
            "FROM services se " \
            "LEFT JOIN books b ON se.service_id = b.service_id " \
            "LEFT JOIN shops sh on b.shop_id = sh.shop_id " \
            "WHERE se.std_name = %s " \
            "AND sh.lat <= %s AND sh.lat >= %s " \
            "AND sh.lng <= %s AND sh.lng >= %s"

    values = [service, max_lat, min_lat, max_long, min_long]
    result = db.execute_select(query, values)

    return result[0]['avg_price'] if result[0]['avg_price'] else 0


#print(get_geo_area_average_service_price('taglio', 40.5913901, 17.10919, 5000))
