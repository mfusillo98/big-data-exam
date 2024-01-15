import classifiers.knn
import classifiers.naive_bayes
import pandas
import csv

def train():
    k = 3
    print(f"Training with k = {k}")
    classifiers.knn.train_model('dataset.train.csv', f"{k}_knn_model.joblib", k)
    print(f"Training completed")


def test():
    k = 3
    df = pandas.read_csv('dataset.full.csv')
    results = []
    for idx in df.index:
        print(f"Computing row {len(results)}")
        results.append({
            "category_tree": df['category_tree'][idx],
            "service_name": df['service_name'][idx],
            "stats_category": classifiers.knn.predict_with_saved_model(
                df['category_tree'][idx],
                df['service_name'][idx],
                f"{k}_knn_model.joblib"
            )
        })

    with open('models/knn/results.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=results[1].keys())
        writer.writeheader()
        writer.writerows(results)
