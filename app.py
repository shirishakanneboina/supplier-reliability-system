
import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# PAGE CONFIGURATION


st.set_page_config(
    page_title="Supplier Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "data/exports/supplier_reliability.db"


# PROFESSIONAL DESIGN


st.markdown("""
<style>
.stApp {
    background: #F3F6FC;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1 {
    color: #142B4A !important;
    font-weight: 800 !important;
    font-size: 34px !important;
}

h2, h3 {
    color: #193B63 !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#142B4A,#203F68);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] input {
    color: #142B4A !important;
    background: white !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E1E8F2;
    box-shadow: 0 4px 14px rgba(20,45,78,0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #173B66 !important;
    font-weight: 800 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #DFE7F1;
    border-radius: 12px;
}

.stButton button, .stDownloadButton button {
    background: #245CA6;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #173B68;
    color: white;
}

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #DFE7F1;
    border-radius: 12px;
}

hr {
    border-color: #DCE5EF !important;
}

</style>
""", unsafe_allow_html=True)


# LOAD DATABASE


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    tables = [
        "suppliers",
        "supplier_scores",
        "shipments",
        "inspections",
        "invoices",
        "risk_signals",
        "purchase_orders",
        "po_lines"
    ]

    data = {}

    for table in tables:
        data[table] = pd.read_sql_query(
            f'SELECT * FROM "{table}"',
            conn
        )

    conn.close()
    return data


if not os.path.exists(DB_PATH):
    st.error("Database not found. Run python src/main.py first.")
    st.stop()

try:
    data = load_data()
except Exception as error:
    st.error(f"Database loading error: {error}")
    st.stop()

suppliers = data["suppliers"]
scores = data["supplier_scores"]
shipments = data["shipments"]
inspections = data["inspections"]
invoices = data["invoices"]
risks = data["risk_signals"]
orders = data["purchase_orders"]
po_lines = data["po_lines"]

report = suppliers.merge(
    scores,
    on="supplier_id",
    how="left"
)

# Ensure numeric scoring values
score_columns = [
    "delivery_score", "quality_score", "cost_score",
    "capacity_score", "compliance_score",
    "risk_score", "overall_score"
]

for col in score_columns:
    report[col] = pd.to_numeric(
        report[col], errors="coerce"
    )

# SIDEBAR NAVIGATION AND FILTERS


st.sidebar.markdown("# 🏢 SUPPLIER")
st.sidebar.markdown("### INTELLIGENCE PLATFORM")
st.sidebar.caption("Performance | Quality | Risk")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Supplier Explorer",
        "Anomaly Monitoring",
        "Data Records"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("🔎 Dashboard Filters")

countries = ["All"] + sorted(
    suppliers["country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

search = st.sidebar.text_input(
    "Search Supplier",
    placeholder="Supplier ID or name..."
)

score_range = st.sidebar.slider(
    "Reliability Score Range",
    min_value=0,
    max_value=100,
    value=(0, 100)
)

filtered = report.copy()

if selected_country != "All":
    filtered = filtered[
        filtered["country"] == selected_country
    ]

if search:
    mask = (
        filtered["supplier_id"].str.contains(
            search, case=False, na=False
        )
        |
        filtered["supplier_name"].str.contains(
            search, case=False, na=False
        )
    )
    filtered = filtered[mask]

filtered = filtered[
    filtered["overall_score"].between(
        score_range[0], score_range[1]
    )
]

filtered_ids = filtered["supplier_id"].dropna().unique()

# Filter related records for the selected supplier population
filtered_shipments = shipments[
    shipments["supplier_id"].isin(filtered_ids)
]

filtered_inspections = inspections[
    inspections["supplier_id"].isin(filtered_ids)
]

filtered_invoices = invoices[
    invoices["supplier_id"].isin(filtered_ids)
]

filtered_risks = risks[
    risks["supplier_id"].isin(filtered_ids)
]

filtered_orders = orders[
    orders["supplier_id"].isin(filtered_ids)
]


# REUSABLE CHART DESIGN


def chart_layout(fig, height=350):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=45, b=25),
        font=dict(
            family="Arial",
            size=12,
            color="#334155"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )
    return fig


def show_empty(message):
    st.info(message)


def metric_row(items):
    columns = st.columns(len(items))

    for column, (label, value) in zip(columns, items):
        column.metric(label, value)


# HEADER


st.markdown("""
# 📊 SUPPLIER RELIABILITY
### ENTERPRISE PERFORMANCE & RISK INTELLIGENCE

A centralized platform for supplier performance,
procurement analytics, quality assurance and risk monitoring.
""")

st.caption(
    "SUPPLIER INTELLIGENCE  •  DATA-DRIVEN DECISIONS  •  "
    "SYNTHETIC DATA"
)

st.divider()


# PAGE 1: EXECUTIVE OVERVIEW


if page == "Executive Overview":

    st.subheader("📌 Executive Overview")

    if filtered.empty:
        st.warning("No suppliers match the selected filters.")
        st.stop()

    average_score = filtered["overall_score"].mean()

    delayed_count = (
        filtered_shipments["status"] == "Delayed"
    ).sum()

    failed_count = (
        filtered_inspections["quality_status"] == "Failed"
    ).sum()

    overdue_count = (
        filtered_invoices["payment_status"] == "Overdue"
    ).sum()

    critical_count = (
        filtered_risks["severity"] == "Critical"
    ).sum()

    # KPI cards
    metric_row([
        ("Total Suppliers", f"{len(filtered):,}"),
        ("Purchase Orders", f"{len(filtered_orders):,}"),
        ("Shipments", f"{len(filtered_shipments):,}"),
        ("Inspections", f"{len(filtered_inspections):,}")
    ])

    st.markdown("")

    metric_row([
        ("Average Reliability", f"{average_score:.2f}/100"),
        ("Delayed Shipments", f"{delayed_count:,}"),
        ("Failed Inspections", f"{failed_count:,}"),
        ("Overdue Invoices", f"{overdue_count:,}")
    ])

    st.divider()

    # Performance analytics
    st.subheader("📈 Performance Analytics")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Supplier Score Distribution")

        distribution = pd.cut(
            filtered["overall_score"],
            bins=[-0.01, 40, 60, 80, 100],
            labels=["Poor", "Average", "Good", "Excellent"]
        ).value_counts().reindex(
            ["Poor", "Average", "Good", "Excellent"],
            fill_value=0
        ).reset_index()

        distribution.columns = ["Category", "Count"]

        fig = px.pie(
            distribution,
            names="Category",
            values="Count",
            hole=0.62,
            color="Category",
            color_discrete_map={
                "Poor": "#EF4444",
                "Average": "#F59E0B",
                "Good": "#3B82F6",
                "Excellent": "#10B981"
            }
        )

        fig.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=3))
        )

        chart_layout(fig)
        st.plotly_chart(fig, width="stretch")

    with right:
        st.markdown("#### Shipment Status")

        shipment_data = (
            filtered_shipments["status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Count")
        )

        if not shipment_data.empty:
            fig = px.bar(
                shipment_data,
                x="Status",
                y="Count",
                color="Status",
                text="Count",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            fig.update_traces(textposition="outside")
            chart_layout(fig)
            st.plotly_chart(fig, width="stretch")
        else:
            show_empty("No shipment records available.")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Inspection Quality")

        quality_data = (
            filtered_inspections["quality_status"]
            .value_counts()
            .rename_axis("Quality")
            .reset_index(name="Count")
        )

        if not quality_data.empty:
            fig = px.pie(
                quality_data,
                names="Quality",
                values="Count",
                hole=0.55,
                color="Quality",
                color_discrete_map={
                    "Passed": "#10B981",
                    "Conditional": "#F59E0B",
                    "Failed": "#EF4444"
                }
            )

            fig.update_traces(textinfo="percent+label")
            chart_layout(fig)
            st.plotly_chart(fig, width="stretch")
        else:
            show_empty("No inspection records available.")

    with right:
        st.markdown("#### Risk Severity")

        risk_data = (
            filtered_risks["severity"]
            .value_counts()
            .rename_axis("Severity")
            .reset_index(name="Count")
        )

        if not risk_data.empty:
            severity_order = ["Low", "Medium", "High", "Critical"]
            risk_data["Severity"] = pd.Categorical(
                risk_data["Severity"],
                categories=severity_order,
                ordered=True
            )
            risk_data = risk_data.sort_values("Severity")

            fig = px.bar(
                risk_data,
                x="Count",
                y="Severity",
                orientation="h",
                color="Severity",
                text="Count",
                color_discrete_map={
                    "Low": "#10B981",
                    "Medium": "#F59E0B",
                    "High": "#F97316",
                    "Critical": "#DC2626"
                }
            )

            fig.update_traces(textposition="outside")
            chart_layout(fig)
            st.plotly_chart(fig, width="stretch")
        else:
            show_empty("No risk records available.")

    st.divider()

    # Rankings
    st.subheader("🏆 Supplier Performance Rankings")

    top, bottom = st.columns(2)

    with top:
        st.markdown("#### ⭐ Top 10 Suppliers")

        st.dataframe(
            filtered.nlargest(10, "overall_score")[
                ["supplier_id", "supplier_name",
                 "country", "overall_score"]
            ],
            width="stretch",
            hide_index=True
        )

    with bottom:
        st.markdown("#### ⚠️ Suppliers Needing Attention")

        st.dataframe(
            filtered.nsmallest(10, "overall_score")[
                ["supplier_id", "supplier_name",
                 "country", "overall_score"]
            ],
            width="stretch",
            hide_index=True
        )

    st.download_button(
        "⬇ Download Executive Supplier Report",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="supplier_executive_report.csv",
        mime="text/csv"
    )

# PAGE 2: SUPPLIER EXPLORER


elif page == "Supplier Explorer":

    st.subheader("🔎 Individual Supplier Analysis")

    if filtered.empty:
        st.warning("No suppliers match your filters.")
        st.stop()

    supplier_ids = sorted(filtered["supplier_id"].dropna().unique())

    selected_supplier = st.selectbox(
        "Choose a Supplier",
        supplier_ids
    )

    supplier = filtered[
        filtered["supplier_id"] == selected_supplier
    ].iloc[0]

    st.divider()

    st.markdown(
        f"## {supplier['supplier_name']} "
        f"({supplier['supplier_id']})"
    )

    a, b, c, d = st.columns(4)

    a.metric("Country", supplier["country"])
    b.metric("Overall Score", f"{supplier['overall_score']:.2f}/100")
    c.metric("Delivery Score", f"{supplier['delivery_score']:.2f}")
    d.metric("Quality Score", f"{supplier['quality_score']:.2f}")

    st.divider()

    st.markdown("#### 📊 Score Component Analysis")

    components = pd.DataFrame({
        "Component": [
            "Delivery", "Quality", "Cost",
            "Capacity", "Compliance", "Risk"
        ],
        "Score": [
            supplier["delivery_score"],
            supplier["quality_score"],
            supplier["cost_score"],
            supplier["capacity_score"],
            supplier["compliance_score"],
            supplier["risk_score"]
        ]
    })

    fig = px.bar(
        components,
        x="Component",
        y="Score",
        color="Score",
        text="Score",
        color_continuous_scale="Blues",
        range_y=[0, 110]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    chart_layout(fig, 400)
    st.plotly_chart(fig, width="stretch")

    st.info(
        f"**Scoring explanation:** {supplier['score_explanation']}"
    )

    # Selected supplier records
    ss = shipments[
        shipments["supplier_id"] == selected_supplier
    ]

    si = inspections[
        inspections["supplier_id"] == selected_supplier
    ]

    sv = invoices[
        invoices["supplier_id"] == selected_supplier
    ]

    sr = risks[
        risks["supplier_id"] == selected_supplier
    ]

    st.divider()
    st.markdown("#### Supplier Business Activity")

    metric_row([
        ("Shipments", len(ss)),
        ("Inspections", len(si)),
        ("Invoices", len(sv)),
        ("Risk Signals", len(sr))
    ])

    with st.expander("🚚 Shipment Records"):
        st.dataframe(ss, width="stretch", hide_index=True)

    with st.expander("🧪 Inspection Records"):
        st.dataframe(si, width="stretch", hide_index=True)

    with st.expander("💰 Invoice Records"):
        st.dataframe(sv, width="stretch", hide_index=True)

    with st.expander("⚠️ Risk Records"):
        st.dataframe(sr, width="stretch", hide_index=True)

    st.download_button(
        "⬇ Download Individual Supplier Report",
        data=supplier.to_frame().T.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected_supplier}_report.csv",
        mime="text/csv"
    )

# =====================================================
# PAGE 3: ANOMALY MONITORING
# =====================================================

elif page == "Anomaly Monitoring":

    st.subheader("🚨 Supplier Anomaly Monitoring")

    st.caption(
        "Monitor unusual delivery, quality, financial and operational events."
    )

    delayed = filtered_shipments[
        filtered_shipments["status"] == "Delayed"
    ]

    failed = filtered_inspections[
        filtered_inspections["quality_status"] == "Failed"
    ]

    overdue = filtered_invoices[
        filtered_invoices["payment_status"] == "Overdue"
    ]

    critical = filtered_risks[
        filtered_risks["severity"] == "Critical"
    ]

    metric_row([
        ("Delivery Delays", f"{len(delayed):,}"),
        ("Quality Failures", f"{len(failed):,}"),
        ("Overdue Invoices", f"{len(overdue):,}"),
        ("Critical Risks", f"{len(critical):,}")
    ])

    st.divider()

    # Anomaly overview
    anomaly_data = pd.DataFrame({
        "Anomaly Type": [
            "Delivery Delays",
            "Quality Failures",
            "Overdue Invoices",
            "Critical Risks"
        ],
        "Records": [
            len(delayed),
            len(failed),
            len(overdue),
            len(critical)
        ]
    })

    fig = px.bar(
        anomaly_data,
        x="Anomaly Type",
        y="Records",
        color="Anomaly Type",
        text="Records",
        color_discrete_sequence=[
            "#F59E0B", "#EF4444", "#8B5CF6", "#B91C1C"
        ]
    )

    fig.update_traces(textposition="outside")
    chart_layout(fig, 380)

    st.plotly_chart(fig, width="stretch")

    st.divider()

    t1, t2, t3, t4 = st.tabs([
        "🚚 Delivery Delays",
        "🧪 Quality Failures",
        "💰 Overdue Invoices",
        "🔴 Critical Risks"
    ])

    with t1:
        st.markdown("#### Delayed Shipment Records")
        st.warning(f"{len(delayed):,} delayed shipment records found.")
        st.dataframe(delayed, width="stretch", hide_index=True)

        st.download_button(
            "Download Delayed Shipments",
            data=delayed.to_csv(index=False).encode("utf-8"),
            file_name="delayed_shipments.csv",
            mime="text/csv",
            key="download_delayed"
        )

    with t2:
        st.markdown("#### Failed Quality Inspections")
        st.error(f"{len(failed):,} failed inspection records found.")
        st.dataframe(failed, width="stretch", hide_index=True)

        st.download_button(
            "Download Failed Inspections",
            data=failed.to_csv(index=False).encode("utf-8"),
            file_name="failed_inspections.csv",
            mime="text/csv",
            key="download_failed"
        )

    with t3:
        st.markdown("#### Overdue Invoice Records")
        st.warning(f"{len(overdue):,} overdue invoices found.")
        st.dataframe(overdue, width="stretch", hide_index=True)

        st.download_button(
            "Download Overdue Invoices",
            data=overdue.to_csv(index=False).encode("utf-8"),
            file_name="overdue_invoices.csv",
            mime="text/csv",
            key="download_overdue"
        )

    with t4:
        st.markdown("#### Critical Supplier Risks")
        st.error(f"{len(critical):,} critical risk signals found.")
        st.dataframe(critical, width="stretch", hide_index=True)

        st.download_button(
            "Download Critical Risks",
            data=critical.to_csv(index=False).encode("utf-8"),
            file_name="critical_risks.csv",
            mime="text/csv",
            key="download_critical"
        )

# =====================================================
# PAGE 4: DATA RECORDS
# =====================================================

elif page == "Data Records":

    st.subheader("🗄️ Business Data Explorer")

    st.caption(
        "Explore the records generated and stored in the SQLite database."
    )

    record_tables = {
        "Suppliers": suppliers[
            suppliers["supplier_id"].isin(filtered_ids)
        ],
        "Supplier Scores": scores[
            scores["supplier_id"].isin(filtered_ids)
        ],
        "Purchase Orders": filtered_orders,
        "Purchase Order Lines": po_lines[
            po_lines["purchase_order_id"].isin(
                filtered_orders["purchase_order_id"]
            )
        ],
        "Shipments": filtered_shipments,
        "Inspections": filtered_inspections,
        "Invoices": filtered_invoices,
        "Risk Signals": filtered_risks
    }

    selected_table = st.selectbox(
        "Select a Data Table",
        list(record_tables.keys())
    )

    selected_data = record_tables[selected_table]

    st.markdown(f"### {selected_table}")

    st.write(f"Total records: **{len(selected_data):,}**")

    st.dataframe(
        selected_data,
        width="stretch",
        hide_index=True
    )

    st.download_button(
        "⬇ Download Selected Data",
        data=selected_data.to_csv(index=False).encode("utf-8"),
        file_name=selected_table.lower().replace(" ", "_") + ".csv",
        mime="text/csv"
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="
    background: #142B4A;
    color: white;
    padding: 22px;
    border-radius: 12px;
    text-align: center;
">
    <h4 style="color:white;margin-bottom:8px;">
        Supplier Reliability Intelligence Platform
    </h4>
    <p style="color:#D5E2F1;margin:0;">
        Synthetic Data | SQLite | Python | Pandas |
        Streamlit | Plotly
    </p>
    <p style="color:#AFC5DF;margin-top:8px;font-size:12px;">
        Supplier Performance • Quality Analytics • Risk Monitoring
    </p>
</div>
""", unsafe_allow_html=True)
