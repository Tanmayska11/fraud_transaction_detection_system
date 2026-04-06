import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

# -------------------------------
# CONFIG
# -------------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

API_URL = os.getenv("API_URL")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

st.set_page_config(page_title="Fraud System", layout="wide")

# =====================================================
# 🎨 GLOBAL CSS
# =====================================================
st.markdown("""
<style>

/* Global container */
.global-box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    border: 2px solid #000;
}

/* Section headers */
.section-header {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    background-color: #f1f1f1;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* KPI styling */
[data-testid="stMetric"] {
    background-color: #f1f1f1;
    border: 2px solid #000;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

[data-testid="stMetricLabel"] {
    justify-content: center;
    font-weight: bold;
}

[data-testid="stMetricValue"] {
    justify-content: center;
}

/* Graph titles */
h3 {
    text-align: center;
    font-weight: bold;
}
            

</style>
""", unsafe_allow_html=True)




# =====================================================
# TITLE
# =====================================================
st.markdown('<div class="section-header">💳 Fraud Detection System</div>', unsafe_allow_html=True)



# =====================================================
# ANALYTICS
# =====================================================
st.markdown('<div class="section-header">📊 Analytics Dashboard</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    query = "SELECT * FROM transactions_raw LIMIT 200000"
    return pd.read_sql(query, engine)

df = load_data()

# KPIs
total = len(df)
fraud = df["isfraud"].sum()
fraud_rate = fraud / total

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", total)
col2.metric("Fraud Cases", fraud)
col3.metric("Fraud Rate", f"{fraud_rate:.2%}")

# =====================================================
# 📊 PLOTLY CHARTS
# =====================================================

def style_fig(fig):
    fig.update_layout(
        
        plot_bgcolor="#f1f1f1",
        paper_bgcolor="#f1f1f1",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(color="black"),
        xaxis=dict(title_font=dict(size=14), showgrid=True),
        yaxis=dict(title_font=dict(size=14), showgrid=True),
    )
    fig.update_traces(marker_line_width=1, marker_line_color="black")
    return fig

# -------------------------------
# Row 1
# -------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Fraud vs Non-Fraud")

    data = df["isfraud"].value_counts().reset_index()
    data.columns = ["Category", "Count"]

    fig = px.bar(data, x="Category", y="Count",
                 labels={"Category": "Transaction Type", "Count": "Number of Transactions"})

    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Fraud by Transaction Type")

    type_counts = df[df["isfraud"] == 1]["type"].value_counts().reset_index()
    type_counts.columns = ["Transaction Type", "Fraud Count"]

    fig = px.bar(type_counts, x="Transaction Type", y="Fraud Count",
                 labels={"Fraud Count": "Number of Fraud Cases"})

    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Row 2
# -------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("Amount Distribution")

    sample_df = df["amount"].sample(2000).reset_index()
    sample_df.columns = ["Index", "Amount"]

    fig = px.line(sample_df, x="Index", y="Amount",labels={"Index": "Transaction Index", "Amount": "Transaction Amount"})

    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("Fraud by Hour")

    df["hour"] = df["step"] % 24
    hourly = df.groupby("hour")["isfraud"].sum().reset_index()
    hourly.columns = ["Hour", "Fraud Count"]

    fig = px.line(hourly, x="Hour", y="Fraud Count",
                  markers=True,
                  labels={"Hour": "Hour of Day", "Fraud Count": "Fraud Cases"})

    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# DETECTION
# =====================================================
st.markdown('<div class="section-header">🔍 Fraud Detection</div>', unsafe_allow_html=True)

col_input, col_result = st.columns([1, 1])

with col_input:
    step = st.number_input("Step", value=1)

    tx_type = st.selectbox(
        "Transaction Type",
        ["CASH_OUT", "TRANSFER", "PAYMENT", "DEBIT", "CASH_IN"]
    )

    amount = st.number_input("Amount", value=1000.0)

    oldbalanceOrg = st.number_input("Old Balance (Sender)", value=0.0)
    newbalanceOrig = st.number_input("New Balance (Sender)", value=0.0)

    oldbalanceDest = st.number_input("Old Balance (Receiver)", value=0.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", value=0.0)

    detect_btn = st.button("🚀 Detect Fraud")

with col_result:
    if detect_btn:
        payload = {
            "step": step,
            "type": tx_type,
            "amount": amount,
            "nameOrig": "CUST001",
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "nameDest": "DEST001",
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest,
            "isFlaggedFraud": 0
        }

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()

                fraud = result["fraud_prediction"]
                prob = result["fraud_probability"]
                reason = result.get("reason", "ML model")

                if fraud == 1:
                    st.error("🚨 FRAUD DETECTED")
                else:
                    st.success("✅ SAFE TRANSACTION")

                st.metric("Fraud Probability", f"{prob:.2%}")
                st.metric("Decision Source", reason)

                st.progress(prob)

            else:
                st.error("API Error")

        except Exception as e:
            st.error(f"Connection Error: {e}")

# =====================================================
# GLOBAL BOX END
# =====================================================
