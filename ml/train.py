from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split

from preprocessing import load_dataset
from model import create_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "sms_spam_model.joblib"


def train_model():
    df = load_dataset()

    X = df["message"]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = create_model()

    print("Training the model...")
    model.fit(X_train, y_train)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("\nTraining completed successfully!")
    print(f"Training messages: {len(X_train)}")
    print(f"Testing messages: {len(X_test)}")
    print(f"Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()

