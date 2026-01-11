import os
import numpy as np
import pandas as pd


def create_feature_dataset(input_path: str, output_path: str) -> None:
    """
    Reads cleaned customer churn data, applies feature engineering,
    and saves featured dataset as CSV.
    """

    df = pd.read_csv(input_path)

    # -----------------------------
    # Tenure groups
    # -----------------------------
    bins = [0, 12, 24, 48, np.inf]
    labels = ["0-12", "12-24", "24-48", "48+"]

    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    # -----------------------------
    # Long-term customer flag
    # -----------------------------
    df["is_long_term_customer"] = (df["tenure"] >= 24).astype(int)

    # -----------------------------
    # Average monthly spend
    # -----------------------------
    df["avg_monthly_spend"] = df["TotalCharges"] / df["tenure"]

    # -----------------------------
    # Multiple services flag
    # -----------------------------
    service_cols = [
        "PhoneService",
        "InternetService",
        "StreamingTV",
        "StreamingMovies",
    ]

    def has_multiple_services(row):
        count = 0

        if row["PhoneService"] == "Yes":
            count += 1

        if row["InternetService"] in ["DSL", "Fiber optic"]:
            count += 1

        if row["StreamingTV"] == "Yes":
            count += 1

        if row["StreamingMovies"] == "Yes":
            count += 1

        return 1 if count >= 2 else 0

    df["multiple_services_flag"] = df.apply(has_multiple_services, axis=1)

    # -----------------------------
    # Save featured dataset
    # -----------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Featured dataset saved to:", output_path)
