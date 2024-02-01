import sys
from classifiers import classifier
from database.querybuilder import QueryBuilder
from preparation import source_data


def main():
    source_qb = QueryBuilder(host='localhost', user='root', password='root', database='bookizon', port=8888)
    dest_qb = QueryBuilder(host='localhost', user='root', password='root', database='bookizon_books_knowledge_discovery', port=8888)
    source_data.import_services(source_qb, dest_qb)
    source_data.import_customers(source_qb, dest_qb)
    source_data.import_shops(source_qb, dest_qb)
    source_data.import_books(source_qb, dest_qb)
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        main()
    elif sys.argv[1] == 'service-classifier-train':
        classifier.train()
    elif sys.argv[1] == 'service-classifier-test':
        classifier.test()
