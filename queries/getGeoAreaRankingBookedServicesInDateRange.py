from app.database.database import get_db
from app.utils.geolocationUtils import sum_km_to_coordinates


'''
2 Ranking dei servizi più prenotati in un area geolocalizzata in un certo periodo dell’anno
'''

def get_geo_area_ranking_booked_services_in_date_range(lat, long, km_radius, date_start, date_end):
    db = get_db()

    max_lat, max_long = sum_km_to_coordinates(lat, long, km_radius)
    min_lat, min_long = sum_km_to_coordinates(lat, long, -km_radius)

    query ="SELECT COUNT(*) as reservation, b.service_id, sr.name " \
          "FROM `books` b " \
          "LEFT JOIN time AS t ON b.book_date_id = t.date_time_id " \
          "LEFT JOIN shops sh on b.shop_id = sh.shop_id " \
          "LEFT JOIN services sr on sr.service_id = b.service_id " \
          "WHERE (CONCAT(t.year, '-', t.month, '-', t.day) BETWEEN %s AND %s) " \
          "AND sh.lat <= %s AND sh.lat >= %s " \
          "AND sh.lng <= %s AND sh.lng >= %s " \
          "GROUP BY b.service_id " \
          "ORDER BY reservation DESC"

    values = [date_start, date_end, max_lat, min_lat, max_long, min_long]
    result = db.execute_select(query, values)

    return result

#print(get_geo_area_ranking_booked_services_in_date_range(40.5913901, 17.10919, 5, "2023-01-01", "2024-01-31"))
