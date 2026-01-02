import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Operational Cost Leakage System",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #eef2ff);
    # color: #e5e7eb;
    # background: #000000;
}

/* Title */
h1 {
    color: #0f172a;
    font-weight: 800;
}

/* Hero text */
h2 {
    color: #0f172a;
}

input{
            color:black
            }

/* Metric cards */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.08);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}
section[data-testid="stSidebar"] * {
    color: white;
}
            
/* File uploader background fix */
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 15px;
    border: 1px dashed #94a3b8;
}

/* File uploader text */
section[data-testid="stSidebar"] div[data-testid="stFileUploader"] * {
    color: white;
}

/* Browse files button */
section[data-testid="stSidebar"] button {
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    color: white;
    border-radius: 10px;
    border: none;
}

                          
</style>
""", unsafe_allow_html=True)


st.title("🚨 Operational Cost Leakage Detection & Optimization System")
st.markdown("""
<div style="
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
">
    <h2>📊 Business Impact Dashboard</h2>
    <p>
    Detect hidden operational cost leakages, identify root causes,
    and apply AI-driven optimization strategies.
    </p>
</div>
""", unsafe_allow_html=True)



# ---------------- SIDEBAR ----------------
st.sidebar.header("Input Options")

input_type = st.sidebar.radio(
    "Choose Input Method",
    ["Upload CSV File", "Manual Simulation"]
)

# ---------------- FUNCTIONS ----------------
def calculate_operational_cost(df):
    traffic_map = {
        "Clear": 1,
        "Heavy": 3,
        "Detour": 4
    }

    df["Traffic_Score"] = df["Traffic_Status"].map(traffic_map).fillna(2)

    df["operational_cost"] = (
        df["Waiting_Time"] * 50 +
        df["Logistics_Delay"] * 100 +
        df["Traffic_Score"] * 200 +
        (100 - df["Asset_Utilization"]) * 10 +
        df["Inventory_Level"] * 2
    )

    return df


def find_root_cause(df):
    reasons = []

    for _, row in df.iterrows():
        cause = []

        if row["Waiting_Time"] > df["Waiting_Time"].mean():
            cause.append("High waiting / idle time")

        if row["Traffic_Score"] >= 3:
            cause.append("Traffic congestion or route detour")

        if row["Asset_Utilization"] < 70:
            cause.append("Low asset utilization")

        if row["Inventory_Level"] > df["Inventory_Level"].mean():
            cause.append("Excess inventory holding")

        if not cause:
            cause.append("Normal operational variation")

        reasons.append(", ".join(cause))

    df["root_cause"] = reasons
    return df


def suggest_optimization(cause):
    solutions = []

    if "waiting" in cause:
        solutions.append("Optimize scheduling to reduce idle time")

    if "Traffic" in cause:
        solutions.append("Use alternative routes or off-peak delivery")

    if "asset" in cause:
        solutions.append("Improve asset allocation and utilization")

    if "inventory" in cause:
        solutions.append("Implement just-in-time inventory management")

    return "; ".join(solutions)


# ---------------- FILE UPLOAD MODE ----------------
if input_type == "Upload CSV File":
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        df = calculate_operational_cost(df)

        features = [
            "Waiting_Time",
            "Logistics_Delay",
            "Traffic_Score",
            "Asset_Utilization",
            "Inventory_Level",
            "operational_cost"
        ]

        model = IsolationForest(
            contamination=0.1,
            random_state=42
        )

        df["anomaly"] = model.fit_predict(df[features])
        df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

        df = find_root_cause(df)

        df["optimization"] = df["root_cause"].apply(suggest_optimization)
        df["potential_savings"] = (df["operational_cost"] * 0.15).round(2)

        # ---------------- METRICS ----------------
        st.subheader("📌 Key Business Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📦 Total Records", len(df))
        col2.metric("🚨 Leakages Detected", int(df["anomaly"].sum()))
        col3.metric("💸 Avg Operational Cost", round(df["operational_cost"].mean(), 2))
        col4.metric("💰 Potential Savings", round(df["potential_savings"].sum(), 2))


        # ---------------- TABLE ----------------
        st.subheader("🚨 Leakage Details")

        show_all = st.checkbox("Show only leakage records", value=True)

        if show_all:
            display_df = df[df["anomaly"] == 1]
        else:
            display_df = df

        st.dataframe(
            display_df[[
                "operational_cost",
                "root_cause",
                "optimization",
                "potential_savings"
            ]],
            use_container_width=True
        )


        # ---------------- CHART ----------------
        # st.subheader("📊 Root Cause Distribution")

        # fig, ax = plt.subplots()
        # df[df["anomaly"] == 1]["root_cause"].value_counts().plot(
        #     kind="bar",
        #     ax=ax
        # )
        # st.pyplot(fig)

        st.subheader("📈 Cost & Root Cause Analysis")

        left, right = st.columns(2)

        with left:
            st.markdown("### 🔴 Leakage Cost Distribution")
            st.scatter_chart(
            df[df["anomaly"] == 1]["operational_cost"]
            )

        with right:
            st.markdown("### 🧠 Root Cause Distribution")
            fig, ax = plt.subplots()
            df[df["anomaly"] == 1]["root_cause"].value_counts().plot(
                kind="bar", ax=ax
            )
            st.pyplot(fig)
        
        st.markdown("---")

        st.success(
            f"✅ By addressing the detected issues, the organization can potentially save "
            f"₹{round(df['potential_savings'].sum(), 2)} in operational costs."
        )

        st.download_button(
            label="⬇️ Download Leakage Analysis Report",
            data=df[df["anomaly"] == 1].to_csv(index=False),
            file_name="operational_cost_leakage_report.csv",
            mime="text/csv"
        )



# ---------------- MANUAL SIMULATION MODE ----------------
else:
    st.sidebar.subheader("Manual Input")

    waiting = st.sidebar.slider("Waiting Time", 0, 100, 30)
    traffic = st.sidebar.selectbox(
        "Traffic Status",
        ["Clear", "Heavy", "Detour"]
    )
    utilization = st.sidebar.slider("Asset Utilization (%)", 0, 100, 70)
    inventory = st.sidebar.slider("Inventory Level", 0, 1000, 300)
    delay = st.sidebar.selectbox("Logistics Delay", [0, 1])

    traffic_score = {
        "Clear": 1,
        "Heavy": 3,
        "Detour": 4
    }[traffic]

    cost = (
        waiting * 50 +
        delay * 100 +
        traffic_score * 200 +
        (100 - utilization) * 10 +
        inventory * 2
    )
    # -------- MANUAL LEAKAGE DETECTION --------
    leakage = False
    manual_causes = []

    if waiting > 40:
        manual_causes.append("High waiting / idle time")

    if traffic_score >= 3:
        manual_causes.append("Traffic congestion or route detour")

    if utilization < 70:
        manual_causes.append("Low asset utilization")

    if inventory > 400:
        manual_causes.append("Excess inventory holding")

    if cost > 3000:
        leakage = True

# Root cause text
    if manual_causes:
        root_cause_text = ", ".join(manual_causes)
    else:
        root_cause_text = "Normal operational variation"

# Optimization
    optimization_text = suggest_optimization(root_cause_text)


    st.metric("Estimated Operational Cost", cost)
    st.markdown(f"""
    <div style="
        background:#020617;
        padding:25px;
        border-radius:16px;
        color:white;
        margin-top:20px;
    ">
    <h3>💸 Estimated Operational Cost</h3>
    <h1>₹ {cost}</h1>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("---")
    st.subheader("🧠 Manual Analysis Result")

    if leakage:
        st.error("🚨 Potential Operational Cost Leakage Detected")
    else:
        st.success("✅ No Major Cost Leakage Detected")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### 🔍 Root Cause")
        st.info(root_cause_text)

    with colB:
        st.markdown("### 🛠 Optimization Suggestion")
        if optimization_text:
            st.success(optimization_text)
        else:
            st.write("Operations are within acceptable limits.")

