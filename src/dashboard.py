import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


# -----------------------------
# Color Theme
# -----------------------------
MAIN_COLOR = "#5FA8A8"
LIGHT_COLOR = "#9ED6D6"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
BORDER_COLOR = "#000000"


# -------------------------------------------------
# Build Churn Dashboard (GitHub Pages Safe)
# -------------------------------------------------
def build_churn_dashboard(csv_dir: str, featured_csv_path: str, output_html_path: str):

    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    # Aggregated CSVs
    df_contract = pd.read_csv(os.path.join(csv_dir, "churn_by_contract.csv"))
    df_tenure = pd.read_csv(os.path.join(csv_dir, "churn_by_tenure.csv"))
    df_payment = pd.read_csv(os.path.join(csv_dir, "churn_by_payment.csv"))
    df_services = pd.read_csv(os.path.join(csv_dir, "churn_by_services.csv"))

    # Featured data for summary
    df_raw = pd.read_csv(featured_csv_path)

    df_services["multiple_services_flag"] = df_services["multiple_services_flag"].replace({
        0: "No", 1: "Yes", "0": "No", "1": "Yes"
    })

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    total_customers = len(df_raw)
    churned_customers = (df_raw["Churn"] == "Yes").sum()
    churn_rate = round((churned_customers / total_customers) * 100, 2)

    # -----------------------------
    # Figure
    # -----------------------------
    fig = go.Figure()
    BAR_WIDTH = 0.45

    fig.add_trace(go.Bar(
        x=df_contract["Contract"],
        y=df_contract["churn_rate"],
        name="Contract",
        marker_color=MAIN_COLOR,
        width=BAR_WIDTH,
        visible=True
    ))

    fig.add_trace(go.Bar(
        x=df_tenure["tenure_group"],
        y=df_tenure["churn_rate"],
        name="Tenure",
        marker_color=MAIN_COLOR,
        width=BAR_WIDTH,
        visible=False
    ))

    fig.add_trace(go.Bar(
        x=df_payment["PaymentMethod"],
        y=df_payment["churn_rate"],
        name="Payment",
        marker_color=MAIN_COLOR,
        width=BAR_WIDTH,
        visible=False
    ))

    fig.add_trace(go.Bar(
        x=df_services["multiple_services_flag"],
        y=df_services["churn_rate"],
        name="Services",
        marker_color=MAIN_COLOR,
        width=BAR_WIDTH,
        visible=False
    ))

    # -----------------------------
    # Layout + Dropdown
    # -----------------------------
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Contract Type",
                        method="update",
                        args=[{"visible": [True, False, False, False]},
                              {"title.text": "Churn Rate by Contract Type"}],
                    ),
                    dict(
                        label="Tenure Group",
                        method="update",
                        args=[{"visible": [False, True, False, False]},
                              {"title.text": "Churn Rate by Tenure Group"}],
                    ),
                    dict(
                        label="Payment Method",
                        method="update",
                        args=[{"visible": [False, False, True, False]},
                              {"title.text": "Churn Rate by Payment Method"}],
                    ),
                    dict(
                        label="Multiple Services",
                        method="update",
                        args=[{"visible": [False, False, False, True]},
                              {"title.text": "Churn Rate by Multiple Services"}],
                    ),
                ],
                direction="down",
                x=0.02,
                y=1.08,
                showactive=True
            )
        ],
        title=dict(text="Churn Rate by Contract Type", x=0.5),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_COLOR),
        margin=dict(t=120),
        yaxis=dict(
            title="Churn Rate (%)",
            gridcolor=GRID_COLOR,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor=BORDER_COLOR,
            mirror=True
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor=BORDER_COLOR,
            mirror=True
        ),
        bargap=0.6
    )

    # -----------------------------
    # Write HTML
    # -----------------------------
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Customer Churn Dashboard</title></head>")
        f.write("<body style='background:#FAFEFE; font-family:Arial;'>")

        f.write("<h1 style='color:#3E7C7C; text-align:center;'>Customer Churn Analysis Dashboard</h1>")

        # Summary Card
        f.write(f"""
        <div style="
            max-width: 500px;
            margin: 20px auto 10px auto;
            padding: 20px;
            border-radius: 16px;
            background-color: #EAF6F6;
            text-align: center;
            color: {DARK_COLOR};
            font-size: 18px;
            line-height: 1.8;
        ">
            <b>Total Customers:</b> {total_customers}<br>
            <b>Churned Customers:</b> {churned_customers}<br>
            <b>Overall Churn Rate:</b> {churn_rate}%
        </div>
        """)

        # Chart Card
        f.write("""
        <div style="
            max-width: 1100px;
            margin: 30px auto;
            padding: 30px;
            border: 1px solid #E6F2F2;
            border-radius: 18px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            background-color: white;
        ">
        """)

        f.write(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))

        f.write("</div></body></html>")

    print("Dashboard created at:", output_html_path)
