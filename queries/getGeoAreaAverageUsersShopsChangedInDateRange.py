from app.database.database import get_db
from app.utils.geolocationUtils import sum_km_to_coordinates

'''
9 Numero medio di attività (dello stesso settore) in cui un cliente prenota nell’arco di 1 anno in un area geolocalizzata
'''


def get_geo_area_average_users_shops_changed_in_date_range(lat, long, km_radius, date_start, date_end):
    db = get_db()

    max_lat, max_long = sum_km_to_coordinates(lat, long, km_radius)
    min_lat, min_long = sum_km_to_coordinates(lat, long, -km_radius)

    query = "SELECT AVG(different_shops) AS average_shops_changed " \
            "FROM ( " \
                "SELECT COUNT(DISTINCT b.shop_id) different_shops " \
                "FROM `books` b " \
                "LEFT JOIN time AS t ON b.book_date_id = t.date_time_id " \
                "LEFT JOIN shops sh on b.shop_id = sh.shop_id " \
                "WHERE (CONCAT(t.year, '-', t.month, '-', t.day) BETWEEN %s AND %s) " \
                "AND sh.lat <= %s AND sh.lat >= %s " \
                "AND sh.lng <= %s AND sh.lng >= %s " \
                "GROUP BY b.customer_id " \
            " ) as sq"

    values = [date_start, date_end, max_lat, min_lat, max_long, min_long]
    result = db.execute_select(query, values)

    return result[0]['average_shops_changed'] if result[0]['average_shops_changed'] else 0



#print(get_geo_area_average_users_shops_changed_in_date_range(40.5913901, 17.10919, 5, "2023-01-01", "2024-01-31"))