from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT / "models" / "sms_spam_model.joblib"
)


def predict_message(message):
    """Classify a message using the saved model."""

    if not message or not message.strip():
        raise ValueError("Please enter a message.")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Run python ml/train.py first."
        )

    model = joblib.load(MODEL_PATH)

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    spam_probability = float(probabilities[1])

    return {
        "prediction": (
            "SPAM" if prediction == 1 else "HAM"
        ),
        "spam_probability": round(spam_probability, 4),
    }


if __name__ == "__main__":
    message = input("Enter a message to analyse: ")

    result = predict_message(message)

    print("\n========== PREDICTION ==========")
    print("Classification:", result["prediction"])
    print(
        "Estimated spam probability:",
        f'{result["spam_probability"]:.2%}',
    )
