from pathlib import Path

import pandas as pd

from sklearn.metrics import classification_report

from preprocessing import load_dataset
from model import create_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_DATA_PATH = (
    PROJECT_ROOT / "data" / "raw" / "cyberguard_examples.csv"
)


def test_cyberguard_examples():
    """Test the model on illustrative CyberGuard examples."""

    if not TEST_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_DATA_PATH}"
        )

    # Load the original SMS spam dataset
    training_data = load_dataset()

    # Load the new CyberGuard examples
    test_data = pd.read_csv(TEST_DATA_PATH)

    required_columns = {"message", "label", "category"}

    if not required_columns.issubset(test_data.columns):
        raise ValueError(
            "CSV must contain message, label, and category columns."
        )

    test_data = test_data.dropna(
        subset=["message", "label", "category"]
    )

    test_data["message"] = (
        test_data["message"].astype(str).str.strip()
    )

    test_data["label"] = (
        test_data["label"].astype(str).str.strip().str.lower()
    )

    test_data = test_data[
        test_data["label"].isin(["scam", "legitimate"])
    ]

    if test_data.empty:
        raise ValueError("No valid test examples were found.")

    # Train using only the original SMS dataset
    model = create_model()

    print("Training model on the original SMS dataset...")
    model.fit(
        training_data["message"],
        training_data["target"],
    )

    # Test on the new examples
    predictions = model.predict(test_data["message"])

    test_data["prediction"] = [
        "scam" if prediction == 1 else "legitimate"
        for prediction in predictions
    ]

    print("\n========== CYBERGUARD TEST RESULTS ==========")

    for _, row in test_data.iterrows():
        print(f"\nCategory: {row['category']}")
        print(f"Message: {row['message']}")
        print(f"Actual label: {row['label']}")
        print(f"Predicted label: {row['prediction']}")

    print("\nClassification Report:")

    print(
        classification_report(
            test_data["label"],
            test_data["prediction"],
            labels=["legitimate", "scam"],
            zero_division=0,
        )
    )

    print(
        "\nNote: This is a tiny illustrative test set, "
        "not a reliable measure of real-world scam detection."
    )


if __name__ == "__main__":
    test_cyberguard_examples()
