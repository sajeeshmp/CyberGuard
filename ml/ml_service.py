from predict import predict_message


def analyze_text(message: str) -> dict:
    """
    Public interface for CyberGuard's ML text classifier.

    Returns the prediction, estimated spam probability,
    explanation, model type, and warning.
    """

    result = predict_message(message)

    return {
        "prediction": result["prediction"],
        "spam_probability": result["spam_probability"],
        "explanation": result["explanation"],
        "model_type": result["model_type"],
        "warning": result["warning"],
    }


if __name__ == "__main__":
    sample = (
        "Your bank account will be blocked. "
        "Verify your KYC immediately."
    )

    output = analyze_text(sample)

    print("CyberGuard ML Service")
    print("---------------------")

    for key, value in output.items():
        print(f"{key}: {value}")