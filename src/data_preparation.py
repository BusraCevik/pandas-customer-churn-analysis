import pandas as pd
import os


def prepare_data(input_path, output_path):
    # Load raw data
    df = pd.read_csv(input_path)

    print("Initial shape:", df.shape)

    # -----------------------------
    # Type conversions
    # -----------------------------
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # -----------------------------
    # Missing values
    # -----------------------------
    missing_before = df.isna().sum()
    print("Missing values before cleaning:\n", missing_before)

 
    df = df.dropna(subset=["TotalCharges"])

    missing_after = df.isna().sum()
    print("Missing values after cleaning:\n", missing_after)

    # -----------------------------
    # Categorical normalization
    # -----------------------------
    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols:
        df[col] = df[col].str.strip()

    # -----------------------------
    # Save cleaned data
    # -----------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Processed data saved to:", output_path)
    print("Final shape:", df.shape)

    return df
