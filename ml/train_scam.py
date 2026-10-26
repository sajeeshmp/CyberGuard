from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from ml.scam_preprocessing import load_scam_dataset
from ml.scam_model import create_scam_model, save_scam_model


def train_scam_model():
    """Train and save CyberGuard's illustrative scam classifier."""

    df = load_scam_dataset()

    X = df["message"]
    y = df["label"]

    # A tiny dataset cannot provide a reliable evaluation.
    # This split is for pipeline demonstration only.
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

    print("\nILLUSTRATIVE TEST RESULTS")
    print("=========================")
    print(f"Training messages: {len(X_train)}")
    print(f"Test messages: {len(X_test)}")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    path = save_scam_model(model)

    print(f"Model saved to: {path}")
    print(
        "\nWarning: This model was trained on a tiny illustrative "
        "dataset and is not ready for real-world scam detection."
    )


if __name__ == "__main__":
    train_scam_model()