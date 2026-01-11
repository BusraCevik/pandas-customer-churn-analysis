import os
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Color Theme
# -----------------------------
MAIN_COLOR = "#5FA8A8"
LIGHT_COLOR = "#9ED6D6"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"

FIG_SIZE = (8, 5)


def _save_bar_plot(df, x_col, y_col, title, ylabel, save_path):
    plt.figure(figsize=FIG_SIZE)

    bars = plt.bar(
        df[x_col],
        df[y_col],
        color=MAIN_COLOR,
        edgecolor=DARK_COLOR,
        width=0.45
    )

    plt.title(title, color=DARK_COLOR)
    plt.ylabel(ylabel, color=DARK_COLOR)
    plt.xlabel(x_col, color=DARK_COLOR)

    plt.grid(axis="y", color=GRID_COLOR)

    plt.xticks(color=DARK_COLOR)
    plt.yticks(color=DARK_COLOR)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2%}",
            ha="center",
            va="bottom",
            color=DARK_COLOR,
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def _plot_churn_by_contract(csv_dir, fig_dir):
    df = pd.read_csv(os.path.join(csv_dir, "churn_by_contract.csv"))

    _save_bar_plot(
        df,
        x_col="Contract",
        y_col="churn_rate",
        title="Churn Rate by Contract Type",
        ylabel="Churn Rate",
        save_path=os.path.join(fig_dir, "churn_by_contract.png"),
    )


def _plot_churn_by_tenure(csv_dir, fig_dir):
    df = pd.read_csv(os.path.join(csv_dir, "churn_by_tenure.csv"))

    _save_bar_plot(
        df,
        x_col="tenure_group",
        y_col="churn_rate",
        title="Churn Rate by Tenure Group",
        ylabel="Churn Rate",
        save_path=os.path.join(fig_dir, "churn_by_tenure.png"),
    )


def _plot_churn_by_payment(csv_dir, fig_dir):
    df = pd.read_csv(os.path.join(csv_dir, "churn_by_payment.csv"))

    _save_bar_plot(
        df,
        x_col="PaymentMethod",
        y_col="churn_rate",
        title="Churn Rate by Payment Method",
        ylabel="Churn Rate",
        save_path=os.path.join(fig_dir, "churn_by_payment.png"),
    )


def _plot_churn_by_services(csv_dir, fig_dir):
    df = pd.read_csv(os.path.join(csv_dir, "churn_by_services.csv"))

    df["multiple_services_flag"] = df["multiple_services_flag"].replace({
        0: "No",
        1: "Yes",
        "0": "No",
        "1": "Yes"
    })

    _save_bar_plot(
        df,
        x_col="multiple_services_flag",
        y_col="churn_rate",
        title="Churn Rate by Multiple Services",
        ylabel="Churn Rate",
        save_path=os.path.join(fig_dir, "churn_by_services.png"),
    )


def generate_visualizations(csv_dir: str, fig_dir: str, doc_path: str) -> None:
    os.makedirs(fig_dir, exist_ok=True)

    _plot_churn_by_contract(csv_dir, fig_dir)
    _plot_churn_by_tenure(csv_dir, fig_dir)
    _plot_churn_by_payment(csv_dir, fig_dir)
    _plot_churn_by_services(csv_dir, fig_dir)

    print("Visualization files created in:", fig_dir)
