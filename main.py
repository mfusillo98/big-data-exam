import sys
from classifiers import classifier


def main():
    # classifier.test()
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        main()
    elif sys.argv[1] == 'service-classifier-train':
        classifier.train()
    elif sys.argv[1] == 'service-classifier-test':
        classifier.test()
