from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from ml.scam_preprocessing import load_scam_dataset
from ml.scam_model import create_scam_model, save_scam_model


def train_scam_model():
    df = load_scam_dataset()
    X = df["message"].astype(str)
    y = df["label"].astype(str).str.strip().str.lower()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    evaluation_model = create_scam_model()
    evaluation_model.fit(X_train, y_train)
    predictions = evaluation_model.predict(X_test)

    print("\nCYBERGUARD SCAM MODEL - EVALUATION")
    print("=================================")
    print(f"Total usable messages: {len(X)}")
    print(f"Training messages: {len(X_train)}")
    print(f"Test messages: {len(X_test)}")
    print(classification_report(y_test, predictions, zero_division=0))

    final_model = create_scam_model()
    final_model.fit(X, y)
    path = save_scam_model(final_model)

    print(f"\nFinal model trained on all {len(X)} usable messages.")
    print(f"Model saved to: {path}")
    print("LIMITATION: This illustrative dataset does not establish real-world performance.")


if __name__ == "__main__":
    train_scam_model()