from app.database.database import get_db
from app.utils.geolocationUtils import sum_km_to_coordinates


'''
4 Categoria di clientela più incentivata dagli sconti per effettuare una prenotazione in un area geolocalizzata
'''

def get_geo_area_gender_discounted_books(lat, long, km_radius):
    db = get_db()

    max_lat, max_long = sum_km_to_coordinates(lat, long, km_radius)
    min_lat, min_long = sum_km_to_coordinates(lat, long, -km_radius)

    query ="SELECT COUNT(*) as reservations, c.gender " \
          "FROM `books` b " \
          "LEFT JOIN customers AS c ON c.customer_id = b.customer_id " \
          "LEFT JOIN shops sh on b.shop_id = sh.shop_id " \
          "WHERE sh.lat <= %s AND sh.lat >= %s " \
          "AND sh.lng <= %s AND sh.lng >= %s " \
          "AND b.discount_price > 0 " \
          "GROUP BY c.gender " \
          "ORDER BY reservations DESC"

    values = [max_lat, min_lat, max_long, min_long]
    result = db.execute_select(query, values)

    return result

print(get_geo_area_gender_discounted_books(40.5913901, 17.10919, 10))
