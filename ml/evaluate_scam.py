from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from scam_preprocessing import load_scam_dataset
from scam_model import create_scam_model


def evaluate_scam_model():
    """Evaluate CyberGuard's illustrative scam classifier."""

    df = load_scam_dataset()

    X = df["message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = create_scam_model()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nCYBERGUARD SCAM MODEL EVALUATION")
    print("================================")

    print(f"Training messages: {len(X_train)}")
    print(f"Test messages: {len(X_test)}")

    print(
        f"\nAccuracy: {accuracy_score(y_test, predictions):.2%}"
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(
        y_test,
        predictions,
        labels=["legitimate", "scam"],
    ))

    print(
        "\nLIMITATION: This evaluation uses a tiny illustrative "
        "dataset. The results do not establish real-world "
        "scam-detection performance."
    )


if __name__ == "__main__":
    evaluate_scam_model()