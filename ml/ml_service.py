from ml.predict import predict_message
from ml.scam_predict import predict_scam


def analyze_text(message: str) -> dict:
    """Analyze a message using the original SMS spam model."""

    return predict_message(message)


def analyze_scam(message: str) -> dict:
    """Analyze a message using CyberGuard's scam classifier."""

    return predict_scam(message)


if __name__ == "__main__":
    test_message = (
        "Police have linked your Aadhaar to a criminal case. "
        "Pay money to avoid arrest."
    )

    print("========== CYBERGUARD ML SERVICE ==========")

    print("\n1. Original SMS spam model:")
    print(analyze_text(test_message))

    print("\n2. CyberGuard scam model:")
    print(analyze_scam(test_message))