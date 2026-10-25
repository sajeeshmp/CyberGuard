from scam_model import load_scam_model


def predict_scam(message: str) -> dict:
    """
    Predict whether a message resembles a scam
    using CyberGuard's illustrative scam classifier.
    """

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Please enter a valid message.")

    model = load_scam_model()

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    classes = list(model.classes_)
    scam_index = classes.index("scam")

    scam_probability = float(probabilities[scam_index])

    return {
        "prediction": prediction,
        "scam_probability": round(scam_probability, 4),
        "explanation": (
            "This is the model's prediction based on patterns "
            "learned from its training data. It is not proof "
            "that the message is fraudulent."
        ),
        "warning": (
            "This model was trained on a tiny illustrative dataset. "
            "Do not rely on it to determine whether a real message "
            "is safe or fraudulent."
        ),
    }


if __name__ == "__main__":
    print("CyberGuard Scam Detection")
    print("-------------------------")

    message = input("Enter a message to analyse: ")

    try:
        result = predict_scam(message)

        print("\nPrediction:", result["prediction"])
        print(
            "Estimated scam probability:",
            f'{result["scam_probability"]:.2%}',
        )
        print("Explanation:", result["explanation"])
        print("Warning:", result["warning"])

    except (ValueError, FileNotFoundError) as error:
        print("Error:", error)