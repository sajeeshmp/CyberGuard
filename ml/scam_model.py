from pathlib import Path

import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT / "models" / "cyberguard_scam_model.joblib"
)


def create_scam_model():
    """Create a text-classification pipeline for scam detection."""

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                sublinear_tf=True,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ])


def save_scam_model(model):
    """Save the trained scam-classification pipeline."""

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(model, MODEL_PATH)

    return MODEL_PATH


def load_scam_model():
    """Load the previously trained scam-classification pipeline."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Scam model not found. Run python ml/train_scam.py first."
        )

    return joblib.load(MODEL_PATH)