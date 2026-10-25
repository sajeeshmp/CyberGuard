from pathlib import Path
import pandas as pd

# Find the CyberGuard project directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Dataset location
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "SMSSpamCollection"


def load_dataset():
    """Load and prepare the SMS Spam Collection dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    # Read the tab-separated dataset
    df = pd.read_csv(
        DATASET_PATH,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8",
    )

    # Remove missing values
    df = df.dropna(subset=["label", "message"])

    # Clean labels and messages
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["message"] = df["message"].astype(str).str.strip()

    # Keep only valid labels
    df = df[df["label"].isin(["ham", "spam"])]

    # Remove empty messages and duplicates
    df = df[df["message"] != ""]
    df = df.drop_duplicates(subset=["label", "message"])

    # Convert labels into numerical values
    df["target"] = df["label"].map({
        "ham": 0,
        "spam": 1,
    })

    if df.empty:
        raise ValueError(
            "The dataset contains no usable messages."
        )

    return df[["message", "label", "target"]]


if __name__ == "__main__":
    dataset = load_dataset()

    print("\nDataset loaded successfully!")
    print(f"Total messages: {len(dataset)}")

    print("\nLabel distribution:")
    print(dataset["label"].value_counts())

    print("\nSample messages:")
    print(dataset.head())

    print("\nMissing values:")
    print(dataset.isnull().sum())
