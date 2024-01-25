from app.database.database import get_db


'''
Prezzo medio di un servizio in un area geolocalizzata
'''
def getGeoAreaAverageServicePrice():
    db = get_db()

    query = "SELECT * FROM books WHERE book_id = %s"
    values = [1]
    projectStored = db.execute_select(query, values)

    print(projectStored)


getGeoAreaAverageServicePrice()