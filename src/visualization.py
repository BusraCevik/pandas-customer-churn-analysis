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


# -------------------------------------------------
# Internal helper
# -------------------------------------------------
def _save_bar_plot(df, x_col, y_col, title, ylabel, save_path):
    plt.figure(figsize=FIG_SIZE)

    bars = plt.bar(
        df[x_col],
        df[y_col],
        color=MAIN_COLOR,
        edgecolor=DARK_COLOR
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


# -------------------------------------------------
# Plot generators
# -------------------------------------------------
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


def _generate_dashboard_html(doc_path: str):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Customer Churn Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #FAFEFE;
            color: #3E7C7C;
            margin: 40px;
            text-align: center;
        }
        h1 { margin-bottom: 20px; }
        select {
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid #5FA8A8;
            font-size: 14px;
            margin-bottom: 25px;
        }
        img {
            max-width: 700px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-top: 10px;
        }
        .stats-box {
            margin-top: 20px;
            background-color: #E6F2F2;
            display: inline-block;
            padding: 15px 25px;
            border-radius: 14px;
            font-size: 14px;
        }
        .stat { margin: 5px 0; }
    </style>
</head>

<body>

<h1>Customer Churn Analysis Dashboard</h1>

<select id="chartSelect">
    <option value="contract">Churn by Contract Type</option>
    <option value="tenure">Churn by Tenure Group</option>
    <option value="payment">Churn by Payment Method</option>
    <option value="services">Churn by Multiple Services</option>
</select>

<div>
    <img id="chartImage" src="../outputs/figures/churn_by_contract.png" alt="chart">
</div>

<div class="stats-box" id="statsBox">
    <div class="stat" id="customerCount"></div>
    <div class="stat" id="churnedCount"></div>
    <div class="stat" id="churnRate"></div>
</div>

<script>
const chartMap = {
    contract: {
        img: "../outputs/figures/churn_by_contract.png",
        csv: "../outputs/csv/churn_by_contract.csv"
    },
    tenure: {
        img: "../outputs/figures/churn_by_tenure.png",
        csv: "../outputs/csv/churn_by_tenure.csv"
    },
    payment: {
        img: "../outputs/figures/churn_by_payment.png",
        csv: "../outputs/csv/churn_by_payment.csv"
    },
    services: {
        img: "../outputs/figures/churn_by_services.png",
        csv: "../outputs/csv/churn_by_services.csv"
    }
};

const chartImage = document.getElementById("chartImage");
const select = document.getElementById("chartSelect");

const customerCountEl = document.getElementById("customerCount");
const churnedCountEl = document.getElementById("churnedCount");
const churnRateEl = document.getElementById("churnRate");

function parseCSV(text) {
    const lines = text.trim().split("\\n");
    const headers = lines[0].split(",");
    const rows = lines.slice(1).map(line => {
        const values = line.split(",");
        const obj = {};
        headers.forEach((h, i) => obj[h] = values[i]);
        return obj;
    });
    return rows;
}

async function updateDashboard(key) {
    const item = chartMap[key];
    chartImage.src = item.img;

    const response = await fetch(item.csv);
    const text = await response.text();
    const rows = parseCSV(text);

    const totalCustomers = rows.reduce((sum, r) => sum + Number(r.customer_count), 0);
    const totalChurned = rows.reduce((sum, r) => sum + Number(r.churned_count), 0);
    const churnRate = totalChurned / totalCustomers;

    customerCountEl.textContent = "Total Customers: " + totalCustomers;
    churnedCountEl.textContent = "Churned Customers: " + totalChurned;
    churnRateEl.textContent = "Overall Churn Rate: " + (churnRate * 100).toFixed(2) + "%";
}

updateDashboard("contract");

select.addEventListener("change", (e) => {
    updateDashboard(e.target.value);
});
</script>

</body>
</html>
"""
    os.makedirs(os.path.dirname(doc_path), exist_ok=True)
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(html_content)


# -------------------------------------------------
# Public API (called from main)
# -------------------------------------------------
def generate_visualizations(csv_dir: str, fig_dir: str, doc_path: str) -> None:
    os.makedirs(fig_dir, exist_ok=True)

    _plot_churn_by_contract(csv_dir, fig_dir)
    _plot_churn_by_tenure(csv_dir, fig_dir)
    _plot_churn_by_payment(csv_dir, fig_dir)
    _plot_churn_by_services(csv_dir, fig_dir)

    _generate_dashboard_html(doc_path)

    print("Visualization files created in:", fig_dir)
    print("Dashboard created at:", doc_path)

