from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT / "data" / "raw" / "cyberguard_training.csv"
)


def load_scam_dataset():
    """Load and validate the CyberGuard scam dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(
        DATASET_PATH,
        encoding="utf-8-sig",
    )

    required_columns = {"message", "label", "category"}

    # Normalize column names to avoid whitespace/case issues.
    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "CSV must contain these columns: "
            "message, label, category. "
            f"Found: {df.columns.tolist()}"
        )

    df = df.dropna(
        subset=["message", "label", "category"]
    ).copy()

    df["message"] = df["message"].astype(str).str.strip()
    df["label"] = (
        df["label"].astype(str).str.strip().str.lower()
    )
    df["category"] = (
        df["category"].astype(str).str.strip().str.lower()
    )

    df = df[df["message"] != ""]

    valid_labels = {"scam", "legitimate"}

    invalid_labels = set(df["label"]) - valid_labels

    if invalid_labels:
        raise ValueError(
            f"Unexpected labels: {sorted(invalid_labels)}"
        )

    if df["label"].nunique() < 2:
        raise ValueError(
            "The dataset must contain both scam and legitimate messages."
        )

    return df.reset_index(drop=True)


if __name__ == "__main__":
    dataset = load_scam_dataset()

    print("CyberGuard scam dataset loaded successfully!")
    print(f"Total messages: {len(dataset)}")
    print("\nLabel distribution:")
    print(dataset["label"].value_counts())
    print("\nCategory distribution:")
    print(dataset["category"].value_counts())