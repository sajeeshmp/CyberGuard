from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

from ml.scam_preprocessing import load_scam_dataset
from ml.scam_model import create_scam_model


def evaluate_scam_model():
    """Evaluate CyberGuard's illustrative scam classifier."""

    df = load_scam_dataset()

    # Validate the required dataset columns.
    required_columns = {"message", "label"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    # Remove empty messages and labels.
    df = df.dropna(subset=["message", "label"]).copy()
    df["message"] = df["message"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df = df[df["message"] != ""]

    # Check the expected labels.
    expected_labels = {"scam", "legitimate"}
    actual_labels = set(df["label"].unique())

    if actual_labels != expected_labels:
        raise ValueError(
            "Expected labels 'scam' and 'legitimate'. "
            f"Found: {sorted(actual_labels)}"
        )

    # Report exact duplicate messages before splitting.
    duplicate_count = int(df["message"].duplicated().sum())

    print("\nCYBERGUARD SCAM MODEL EVALUATION")
    print("================================")
    print(f"Usable messages: {len(df)}")
    print(f"Scam messages: {(df['label'] == 'scam').sum()}")
    print(f"Legitimate messages: {(df['label'] == 'legitimate').sum()}")
    print(f"Repeated message rows: {duplicate_count}")

    if duplicate_count:
        print(
            "WARNING: Repeated messages exist. Check whether "
            "duplicates could affect evaluation."
        )

    X = df["message"]
    y = df["label"]

    # Keep a held-out test set for final evaluation.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = create_scam_model()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print(f"\nTraining messages: {len(X_train)}")
    print(f"Test messages: {len(X_test)}")
    print(f"\nAccuracy: {accuracy_score(y_test, predictions):.2%}")
    print(f"Scam precision: {precision_score(y_test, predictions, pos_label='scam', zero_division=0):.2%}")
    print(f"Scam recall: {recall_score(y_test, predictions, pos_label='scam', zero_division=0):.2%}")
    print(f"Scam F1-score: {f1_score(y_test, predictions, pos_label='scam', zero_division=0):.2%}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=["legitimate", "scam"],
            zero_division=0,
        )
    )

    print("Confusion Matrix (rows = actual, columns = predicted):")
    print("Labels: legitimate, scam")
    print(
        confusion_matrix(
            y_test,
            predictions,
            labels=["legitimate", "scam"],
        )
    )

    # Cross-validation on the training portion only.
    # Five folds require at least five examples of each class in training.
    class_counts = y_train.value_counts()

    if len(class_counts) == 2 and class_counts.min() >= 5:
        folds = min(5, int(class_counts.min()))
        cv = StratifiedKFold(
            n_splits=folds,
            shuffle=True,
            random_state=42,
        )

        cv_model = create_scam_model()
        cv_scores = cross_val_score(
            cv_model,
            X_train,
            y_train,
            cv=cv,
            scoring="f1_macro",
        )

        print(f"\n{folds}-fold cross-validation macro F1:")
        print("Scores:", [round(score, 3) for score in cv_scores])
        print(f"Mean macro F1: {cv_scores.mean():.2%}")
    else:
        print(
            "\nCross-validation skipped: there are too few examples "
            "per class in the training split."
        )

    print(
        "\nLIMITATION: Results from a small illustrative dataset "
        "are highly uncertain and do not establish real-world "
        "scam-detection performance. Test with larger, diverse, "
        "representative data before relying on this model."
    )


if __name__ == "__main__":
    evaluate_scam_model()