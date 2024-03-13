import sys
from classifiers import classifier
from database.querybuilder import QueryBuilder
from preparation import source_data
from queries.getGeoAreaAverageServicePrice import get_geo_area_average_service_price
from queries.getGeoAreaAverageUsersBooksInDateRange import get_geo_area_average_users_books_in_date_range
from queries.getGeoAreaAverageUsersShopsChangedInDateRange import get_geo_area_average_users_shops_changed_in_date_range
from queries.getGeoAreaBestDaysHoursForBooks import get_geo_area_best_days_hours_for_books
from queries.getGeoAreaBestDaysHoursServiceForBooks import get_geo_area_best_days_hours_service_for_books
from queries.getGeoAreaBestDaysHoursToBook import get_geo_area_best_days_hours_to_book
from queries.getGeoAreaGenderDiscountedBooks import get_geo_area_gender_discounted_books
from queries.getGeoAreaRankingBookedServicesInDateRange import get_geo_area_ranking_booked_services_in_date_range
from queries.getGeoAreaRankingDiscountedServicesInDateRange import \
    get_geo_area_ranking_discounted_services_in_date_range


def main():
    lat = 40.5913901
    long = 17.10919
    km_radius = 50

    service = 'taglio'

    start_date = "2023-10-01"
    end_date = "2024-01-31"

    print("Average price of services in a Geographical Area:",
          get_geo_area_average_service_price(service, lat, long, km_radius), "\n")

    print("Ranking of most booked services in a geographical area during a specific Period:",
          get_geo_area_ranking_booked_services_in_date_range(lat, long, km_radius, start_date, end_date), "\n")

    print("Ranking of most discounted services in a geographical area during a specific Period:",
          get_geo_area_ranking_discounted_services_in_date_range(lat, long, km_radius, start_date, end_date), "\n")

    print("Customer category incentivized by discounts in a geographical area:",
          get_geo_area_gender_discounted_books(lat, long, km_radius), "\n")

    print("Day of week and time slot FOR book in a geographical area:",
          get_geo_area_best_days_hours_for_books(lat, long, km_radius), "\n")

    print("Day of week and time slot TO book in a geographical Area:",
          get_geo_area_best_days_hours_to_book(lat, long, km_radius), "\n")

    print("Day of week and time slot TO book in a geographical Area with specific service:",
          get_geo_area_best_days_hours_service_for_books(lat, long, km_radius), "\n")

    print("Average number of reservations of a user in a date range in a geographical Area:",
          get_geo_area_average_users_books_in_date_range(lat, long, km_radius, start_date, end_date), "\n")

    print("Average price of services in a Geographical Area:",
          get_geo_area_average_users_shops_changed_in_date_range(lat, long, km_radius, start_date, end_date), "\n")

    '''
    source_qb = QueryBuilder(host='localhost', user='root', password='root', database='bookizon_app', port=8889)
    dest_qb = QueryBuilder(host='localhost', user='root', password='root',
                                     database='bookizon_books_knowledge_discovery', port=8889)
    source_data.import_services(source_qb, dest_qb)
    source_data.import_customers(source_qb, dest_qb)
    source_data.import_shops(source_qb, dest_qb)
    source_data.import_books(source_qb, dest_qb)
    pass'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    '''
        if len(sys.argv) < 2:
        main()
    elif sys.argv[1] == 'service-classifier-train':
        classifier.train()
    elif sys.argv[1] == 'service-classifier-test':
        classifier.test()
    '''
