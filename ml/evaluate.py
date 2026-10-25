from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split

from preprocessing import load_dataset
from model import create_model


def evaluate_model():
    """Evaluate the model on unseen test messages."""

    # Load the dataset
    df = load_dataset()

    X = df["message"]
    y = df["target"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # Train a fresh model for evaluation
    model = create_model()

    print("Training model for evaluation...")
    model.fit(X_train, y_train)

    # Predict labels for unseen test messages
    predictions = model.predict(X_test)

    # Display evaluation results
    print("\n========== MODEL EVALUATION ==========")

    accuracy = accuracy_score(y_test, predictions)
    print(f"\nAccuracy: {accuracy:.2%}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Ham (Legitimate)", "Spam"],
            zero_division=0,
        )
    )

    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions,
            labels=[0, 1],
        )
    )


if __name__ == "__main__":
    evaluate_model()
