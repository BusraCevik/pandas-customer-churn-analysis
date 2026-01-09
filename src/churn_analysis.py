import os
import pandas as pd


def compute_churn_metrics(input_path: str, output_dir: str) -> None:
    """
    Computes churn metrics and saves summary CSV files
    for dashboard visualizations.
    """

    df = pd.read_csv(input_path)

    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # Overall churn KPI
    # -----------------------------
    total_customers = len(df)
    churned_customers = (df["Churn"] == "Yes").sum()
    churn_rate = churned_customers / total_customers

    overall_kpi = pd.DataFrame([{
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate
    }])

    overall_kpi.to_csv(os.path.join(output_dir, "overall_kpi.csv"), index=False)

    # -----------------------------
    # Churn by Contract
    # -----------------------------
    churn_by_contract = (
        df.groupby("Contract")
        .apply(lambda x: (x["Churn"] == "Yes").mean())
        .reset_index(name="churn_rate")
    )

    churn_by_contract["customer_count"] = df.groupby("Contract").size().values

    churn_by_contract.to_csv(
        os.path.join(output_dir, "churn_by_contract.csv"),
        index=False
    )

    # -----------------------------
    # Churn by Tenure Group
    # -----------------------------
    churn_by_tenure = (
        df.groupby("tenure_group")
        .apply(lambda x: (x["Churn"] == "Yes").mean())
        .reset_index(name="churn_rate")
    )

    churn_by_tenure["customer_count"] = df.groupby("tenure_group").size().values

    churn_by_tenure.to_csv(
        os.path.join(output_dir, "churn_by_tenure.csv"),
        index=False
    )

    # -----------------------------
    # Churn by Payment Method
    # -----------------------------
    churn_by_payment = (
        df.groupby("PaymentMethod")
        .apply(lambda x: (x["Churn"] == "Yes").mean())
        .reset_index(name="churn_rate")
    )

    churn_by_payment.to_csv(
        os.path.join(output_dir, "churn_by_payment.csv"),
        index=False
    )

    # -----------------------------
    # Churn by Multiple Services Flag
    # -----------------------------
    churn_by_services = (
        df.groupby("multiple_services_flag")
        .apply(lambda x: (x["Churn"] == "Yes").mean())
        .reset_index(name="churn_rate")
    )

    churn_by_services.to_csv(
        os.path.join(output_dir, "churn_by_services.csv"),
        index=False
    )

    print("Churn analysis summaries saved to:", output_dir)
