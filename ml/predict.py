from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT / "models" / "sms_spam_model.joblib"
)


def predict_message(message):
    """
    Classify a message using the trained SMS spam model.

    Returns the prediction, estimated spam probability,
    and an explanation of the result.
    """

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Please enter a valid message.")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. "
            "Run: python ml/train.py"
        )

    # Load the trained model
    model = joblib.load(MODEL_PATH)

    # Predict the message class
    prediction = model.predict([message])[0]

    # Get probabilities associated with each class
    probabilities = model.predict_proba([message])[0]

    # Identify the spam class instead of assuming its position
    classes = list(model.classes_)

    if 1 not in classes:
        raise ValueError(
            "The trained model does not contain the spam class."
        )

    spam_index = classes.index(1)
    spam_probability = float(probabilities[spam_index])

    if prediction == 1:
        classification = "SPAM"
        explanation = (
            "The model classified this message as spam "
            "based on patterns learned from its training data."
        )
    else:
        classification = "HAM"
        explanation = (
            "The model classified this message as legitimate-like "
            "based on patterns learned from its training data."
        )

    return {
        "prediction": classification,
        "spam_probability": round(spam_probability, 4),
        "explanation": explanation,
        "model_type": "SMS spam classifier",
        "warning": (
            "This prediction is not a definitive scam verdict. "
            "A low spam probability does not guarantee safety, "
            "and a high probability does not prove fraud."
        ),
    }


if __name__ == "__main__":
    message = input("Enter a message to analyse: ")

    try:
        result = predict_message(message)

        print("\n========== CYBERGUARD ML RESULT ==========")
        print("Classification:", result["prediction"])
        print(
            "Estimated spam probability:",
            f'{result["spam_probability"]:.2%}',
        )
        print("Explanation:", result["explanation"])
        print("Model type:", result["model_type"])
        print("Warning:", result["warning"])

    except (ValueError, FileNotFoundError) as error:
        print("Error:", error)