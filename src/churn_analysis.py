import os
import pandas as pd


def compute_churn_metrics(input_path: str, output_dir: str) -> None:
    """
    Reads featured customer dataset and computes churn metrics
    by different customer segments. Outputs summary CSV files
    for dashboard visualizations.
    """

    df = pd.read_csv(input_path)

    # -------------------------------------------------
    # Overall churn KPI(Key Performance Indicator)
    # -------------------------------------------------
    total_customers = len(df)
    churned_customers = (df["Churn"] == "Yes").sum()
    churn_rate = churned_customers / total_customers

    overall_kpi = pd.DataFrame([{
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate
    }])

    overall_kpi.to_csv(
        os.path.join(output_dir, "overall_kpi.csv"),
        index=False
    )

    # -------------------------------------------------
    # Churn by Contract Type
    # -------------------------------------------------
    churn_by_contract = (
        df.groupby("Contract")
          .agg(
              churned_count=("Churn", lambda x: (x == "Yes").sum()),
              customer_count=("Churn", "size"),
              churn_rate=("Churn", lambda x: (x == "Yes").mean())
          )
          .reset_index()
    )

    churn_by_contract.to_csv(
        os.path.join(output_dir, "churn_by_contract.csv"),
        index=False
    )

    # -------------------------------------------------
    # Churn by Tenure Group
    # -------------------------------------------------
    churn_by_tenure = (
        df.groupby("tenure_group")
          .agg(
              churned_count=("Churn", lambda x: (x == "Yes").sum()),
              customer_count=("Churn", "size"),
              churn_rate=("Churn", lambda x: (x == "Yes").mean())
          )
          .reset_index()
    )

    churn_by_tenure.to_csv(
        os.path.join(output_dir, "churn_by_tenure.csv"),
        index=False
    )

    # -------------------------------------------------
    # Churn by Payment Method
    # -------------------------------------------------
    churn_by_payment = (
        df.groupby("PaymentMethod")
          .agg(
              churned_count=("Churn", lambda x: (x == "Yes").sum()),
              customer_count=("Churn", "size"),
              churn_rate=("Churn", lambda x: (x == "Yes").mean())
          )
          .reset_index()
    )

    churn_by_payment.to_csv(
        os.path.join(output_dir, "churn_by_payment.csv"),
        index=False
    )

    # -------------------------------------------------
    # Churn by Multiple Services Flag
    # -------------------------------------------------
    churn_by_services = (
        df.groupby("multiple_services_flag")
          .agg(
              churned_count=("Churn", lambda x: (x == "Yes").sum()),
              customer_count=("Churn", "size"),
              churn_rate=("Churn", lambda x: (x == "Yes").mean())
          )
          .reset_index()
    )

    churn_by_services.to_csv(
        os.path.join(output_dir, "churn_by_services.csv"),
        index=False
    )

    print("Churn analysis summary CSV files created in:", output_dir)
