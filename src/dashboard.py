import os
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


MAIN_COLOR = "#5FA8A8"
DARK_COLOR = "#3E7C7C"
GRID_COLOR = "#E6F2F2"
BORDER_COLOR = "#000000"


def build_churn_dashboard(csv_dir: str, featured_csv_path: str, output_html_path: str):

    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    df_contract = pd.read_csv(os.path.join(csv_dir, "churn_by_contract.csv"))
    df_tenure = pd.read_csv(os.path.join(csv_dir, "churn_by_tenure.csv"))
    df_payment = pd.read_csv(os.path.join(csv_dir, "churn_by_payment.csv"))
    df_services = pd.read_csv(os.path.join(csv_dir, "churn_by_services.csv"))

    df_raw = pd.read_csv(featured_csv_path)

    df_services["multiple_services_flag"] = df_services["multiple_services_flag"].replace({
        0: "No", 1: "Yes", "0": "No", "1": "Yes"
    })

    # -----------------------------
    # Summary
    # -----------------------------
    total_customers = len(df_raw)
    churned_customers = (df_raw["Churn"] == "Yes").sum()
    churn_rate = round((churned_customers / total_customers) * 100, 2)

    # -----------------------------
    # Figure
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_contract["Contract"],
        y=df_contract["churn_rate"],
        name="Contract",
        marker_color=MAIN_COLOR,
        visible=True
    ))

    fig.add_trace(go.Bar(
        x=df_tenure["tenure_group"],
        y=df_tenure["churn_rate"],
        name="Tenure",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    fig.add_trace(go.Bar(
        x=df_payment["PaymentMethod"],
        y=df_payment["churn_rate"],
        name="Payment",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    fig.add_trace(go.Bar(
        x=df_services["multiple_services_flag"],
        y=df_services["churn_rate"],
        name="Services",
        marker_color=MAIN_COLOR,
        visible=False
    ))

    fig.update_layout(
        title=dict(text="Churn Rate by Contract Type", x=0.5),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_COLOR),
        margin=dict(t=80),
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

    plot_html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn", div_id="churnChart")

    # -----------------------------
    # Write HTML
    # -----------------------------
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(f"""
<html>
<head>
<title>Customer Churn Dashboard</title>
</head>

<body style="background:#FAFEFE; font-family:Arial;">

<h1 style="color:{DARK_COLOR}; text-align:center;">
Customer Churn Analysis Dashboard
</h1>

<!-- SUMMARY CARD -->
<div style="
    max-width: 500px;
    margin: 20px auto;
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

<!-- DROPDOWN OUTSIDE CARD -->
<div style="text-align:center; margin-top:20px;">
<select id="metricSelect" style="
    padding:10px 16px;
    border-radius:10px;
    border:1px solid #BFDCDC;
    font-size:15px;
    color:{DARK_COLOR};
" onchange="updateChart()">
    <option value="0">Contract Type</option>
    <option value="1">Tenure Group</option>
    <option value="2">Payment Method</option>
    <option value="3">Multiple Services</option>
</select>
</div>

<!-- GRAPH CARD -->
<div style="
    max-width: 1100px;
    margin: 25px auto;
    padding: 30px;
    border: 1px solid #E6F2F2;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    background-color: white;
">
{plot_html}
</div>

<script>
function updateChart() {{
    const val = document.getElementById("metricSelect").value;
    let visibility = [false, false, false, false];
    visibility[val] = true;

    let titles = [
        "Churn Rate by Contract Type",
        "Churn Rate by Tenure Group",
        "Churn Rate by Payment Method",
        "Churn Rate by Multiple Services"
    ];

    Plotly.restyle("churnChart", "visible", visibility);
    Plotly.relayout("churnChart", {{
        title: {{ text: titles[val], x: 0.5 }}
    }});
}}
</script>

</body>
</html>
""")

    print("Dashboard created at:", output_html_path)
