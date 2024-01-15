import joblib  # Import joblib for model persistence
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier

from classifiers.preprocessor import preprocess_text


def train_model(train_file, model_save_path, n_neighbors=3):
    """
    Train a k-NN model on the provided training data and save the model to a file.

    Parameters:
    - train_file (str): Path to the CSV file containing training data.
    - model_save_path (str): Path to save the trained k-NN model.

    Returns:
    None
    """
    # Load training data from CSV file
    train_df = pd.read_csv(train_file)

    # Drop rows with missing values in 'category_tree' or 'service_name' columns
    train_df = train_df.dropna(subset=['category_tree', 'service_name', 'stats_category'])

    # Preprocess text data to be case-insensitive
    train_df['category_tree'] = train_df['category_tree'].apply(preprocess_text)
    train_df['service_name'] = train_df['service_name'].apply(preprocess_text)
    train_df['stats_category'] = train_df['stats_category'].apply(preprocess_text)


    # Extract features (X) and labels (y) from the training DataFrame
    # X_train = train_df['category_tree'] + ' > ' + train_df['service_name']
    X_train = train_df['service_name']
    y_train = train_df['stats_category']

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)

    # Train a k-NN classifier
    knn_model = KNeighborsClassifier(n_neighbors=n_neighbors, metric='cosine')
    knn_model.fit(X_train_tfidf, y_train)

    # Save the trained model to a file using joblib
    joblib.dump((vectorizer, knn_model), model_save_path)
    print(f"Model trained and saved to {model_save_path}")


def predict_with_saved_model(category_tree, service_name, model_load_path):
    """
    Load a pre-trained k-NN model and make predictions on new data.

    Parameters:
    - category_tree (str): The category tree of the service.
    - service_name (str): The name of the service.
    - model_load_path (str): Path to load the pre-trained k-NN model.

    Returns:
    str: Predicted basic name for the given input.
    """
    # Load the trained model from a file using joblib
    vectorizer, knn_model = joblib.load(model_load_path)

    # Transform input data using the vectorizer
    input_text = f"{category_tree.lower()} > {service_name.lower()}"
    input_tfidf = vectorizer.transform([input_text])

    # Make predictions on the input data
    predicted_basic_name = knn_model.predict(input_tfidf)[0]

    return predicted_basic_name


def evaluate_model_on_test_data(test_file, model_load_path):
    """
    Load a pre-trained k-NN model, evaluate its performance on test data,
    and display model performance metrics.

    Parameters:
    - test_file (str): Path to the CSV file containing test data.
    - model_load_path (str): Path to load the pre-trained k-NN model.

    Returns:
    None
    """
    # Load testing data from CSV file
    test_df = pd.read_csv(test_file)

    # Drop rows with missing values in 'category_tree' or 'service_name' columns
    test_df = test_df.dropna(subset=['category_tree', 'service_name'])
    # Preprocess text data to be case-insensitive
    test_df['category_tree'] = test_df['category_tree'].apply(preprocess_text)
    test_df['service_name'] = test_df['service_name'].apply(preprocess_text)
    test_df['stats_category'] = test_df['stats_category'].apply(preprocess_text)

    # Extract features (X) and labels (y) from the testing DataFrame
    X_test = test_df['category_tree'] + ' > ' + test_df['service_name']
    y_test = test_df['stats_category']

    # Load the trained model from a file using joblib
    vectorizer, knn_model = joblib.load(model_load_path)

    # Transform test data using the vectorizer
    X_test_tfidf = vectorizer.transform(X_test)

    # Make predictions on the test set
    predictions = knn_model.predict(X_test_tfidf)

    # Evaluate the model
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")

    # Display classification report
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))
