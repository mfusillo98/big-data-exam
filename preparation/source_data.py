import classifiers.knn
from datetime import datetime, date


def import_services(source_qb, dest_qb):
    # Fetching results
    results = source_qb.select('booking_servizi',
                               columns="id_servizio as id, nome as name, CATEGORIA_SERVIZI_PATH(categoria, ' > ') as category").fetch_all()
    for row in results:
        print(f"Estimating std name for {row['name']}")
        std_name = classifiers.knn.predict_with_saved_model(
            row['category'],
            row['name'],
            f"3_knn_model.joblib"
        )
        new_user_data = {'service_id': row['id'], 'name': row['name'], 'category': row['category'],
                         'std_name': std_name}
        dest_qb.insert('services', new_user_data).execute()
        print(f"Inserted {std_name}")


def get_date_time_id(date_time_str, dest_qb):
    """
    Returns the date time id in the datawarehouse DB based on a date
    :param date_time_str: format Y-m-d H:i:s
    :return: int
    """
    date_time_obj = date_time_str if isinstance(date_time_str, datetime) else datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    y = date_time_obj.year
    m = date_time_obj.month
    d = date_time_obj.day
    hh = date_time_obj.hour
    mm = date_time_obj.minute

    row = dest_qb.select('time', columns='date_time_id').where(
        f"year = {y} AND month={m} AND day = {d} AND hour = {hh} and minutes = {mm}").fetch_one()
    if row is not None:
        return row['date_time_id']
    new_time_data = {'year': y, 'month': m, 'day': d, 'hour': hh, 'minutes': mm}
    return dest_qb.insert('time', new_time_data).execute(return_lastrowid=True)


def parse_datetime(input_str, date_formats):
    if input_str is not None:
        for date_format in date_formats:
            try:
                dt_object = datetime.strptime(input_str, date_format)
                return dt_object.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass  # Continue to the next format if parsing fails

    # If no format matches, raise an exception or return None
    raise ValueError(f"Unable to parse the input string: {input_str}")


def import_customers(source_qb, dest_qb):
    # Fetching results
    results = source_qb.select('booking_utenti',
                               columns="id_utente as id, sesso as gender, data_nascita as birthday").fetch_all()
    for row in results:

        try:
            birthday_date_time_id = get_date_time_id(parse_datetime(row['birthday'], ["%Y-%m-%d", "%d-%m-%Y"]), dest_qb)
        except ValueError as e:
            birthday_date_time_id = None
        new_user_data = {'customer_id': row['id'], 'gender': row['gender'],
                         'birthday_date_time_id': birthday_date_time_id}
        dest_qb.insert('customers', new_user_data).execute()
        print(f"Inserted {row['id']}")


def import_shops(source_qb, dest_qb):
    # Fetching results
    results = source_qb.select('booking_sedi',
                               columns="id_sede as shop_id, lat, lng").fetch_all()
    for row in results:
        dest_qb.insert('shops', row).execute()
        print(f"Inserted {row['shop_id']}")


def import_books(source_qb, dest_qb):
    # Fetching results
    results = source_qb.select('booking_prenotazioni', columns="*").fetch_all()
    for row in results:
        if row['id_utente'] is None:
            continue
        if row['date_ymd'] is None:
            continue
        if row['data_creazione'] is None:
            continue

        customer = dest_qb.select('customers', columns='birthday_date_time_id').where(f"customer_id = {row['id_utente']}").fetch_one()
        if customer is None:
            continue

        customer_age = None
        if customer['birthday_date_time_id'] is not None:
            birthday_date_time = dest_qb.select('time', columns='*').where(f"date_time_id = {customer['birthday_date_time_id']}").fetch_one()
            if birthday_date_time is not None:
                birthday_date = date(int(birthday_date_time['year']), int(birthday_date_time['month']), int(birthday_date_time['day']))
                book_creation_date = row['data_creazione']
                customer_age = book_creation_date.year - birthday_date.year - ((book_creation_date.month, book_creation_date.day) < (birthday_date.month, birthday_date.day))

        # Book creation date time id
        try:
            book_creation_date_id = get_date_time_id(row['data_creazione'], dest_qb)
        except ValueError as e:
            book_creation_date_id = None

        # Book execution date time id
        try:
            book_date_id = get_date_time_id(parse_datetime(row['date_ymd'].strftime("%Y-%m-%d") + ' ' + row['orario'], ["%Y-%m-%d %H:%M"]),
                                            dest_qb)
        except ValueError as e:
            book_date_id = None

        price = float(row['prezzo_servizio_base'] if row['prezzo_servizio_base'] is not None else 0)
        discount_perc = float(row['perc_sconto_servizio']   if row['perc_sconto_servizio'] is not None else 0)
        discounted_price = price - (price * discount_perc / 100)

        book_data = {
            "book_id": row['id_prenotazione'],
            "service_id": row['id_servizio'],
            "book_creation_date_id": book_creation_date_id,
            "book_date_id": book_date_id,
            "customer_id": row['id_utente'],
            "shop_id": row['id_sede'],
            "price": price,
            "discount_price": discounted_price,
            "discount_perc": discount_perc,
            "duration": int(row['durata']) * 5,
            "customer_age": customer_age,
            # "platform": row['id_prenotazione']
            # "place_id": row['id_prenotazione']
        }
        dest_qb.insert('books', book_data).execute()
        print(f"Inserted {book_data['book_id']}")
