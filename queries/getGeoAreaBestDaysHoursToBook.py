from app.database.database import get_db
from app.utils.geolocationUtils import sum_km_to_coordinates


'''
5 Fascia oraria e giorno della settimana in cui vengono effettuate più prenotazioni (intesa come l’azione di prenotare, e non l’esecuzione del servizio) in un area geolocalizzata
'''

def get_geo_area_best_days_hours_to_book(lat, long, km_radius):
    db = get_db()

    max_lat, max_long = sum_km_to_coordinates(lat, long, km_radius)
    min_lat, min_long = sum_km_to_coordinates(lat, long, -km_radius)

    query ="SELECT COUNT(*) as reservations, t.day_of_week, t.hour " \
          "FROM `books` b " \
          "LEFT JOIN time AS t ON b.book_creation_date_id = t.date_time_id " \
          "LEFT JOIN shops sh on b.shop_id = sh.shop_id " \
          "WHERE sh.lat <= %s AND sh.lat >= %s " \
          "AND sh.lng <= %s AND sh.lng >= %s " \
          "GROUP BY t.day_of_week, t.hour " \
          "ORDER BY reservations DESC " \
          "LIMIT 10 "

    values = [max_lat, min_lat, max_long, min_long]
    result = db.execute_select(query, values)

    return result

#print(get_geo_area_best_days_hours_to_book(40.5913901, 17.10919, 10))
