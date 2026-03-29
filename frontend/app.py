import streamlit as st
import pandas as pd
import os

from components.charts import line_chart, heatmap, scatter
from components.metrics import get_metrics

st.set_page_config(layout="wide")
st.title("AlphaPulse Dashboard")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RETURNS_PATH = os.path.join(BASE_DIR, "backend", "data", "processed", "returns.csv")
CORR_PATH = os.path.join(BASE_DIR, "backend", "data", "processed", "correlation.csv")
MC_PATH = os.path.join(BASE_DIR, "backend", "data", "processed", "monte_carlo.csv")

# ✅ Safety check
if not os.path.exists(RETURNS_PATH):
    st.error("⚠️ Data not found. Please run backend first.")
    st.stop()

returns = pd.read_csv(RETURNS_PATH, index_col=0)
corr = pd.read_csv(CORR_PATH, index_col=0)
mc = pd.read_csv(MC_PATH)

# ================= UI =================

st.subheader("Returns")
st.plotly_chart(line_chart(returns), width="stretch")

st.subheader("Correlation")
st.plotly_chart(heatmap(corr), width="stretch")

st.subheader("Monte Carlo")
st.plotly_chart(scatter(mc), width="stretch")

metrics = get_metrics(mc)

col1, col2, col3 = st.columns(3)
col1.metric("Avg Return", metrics["avg_return"])
col2.metric("Avg Risk", metrics["avg_risk"])
col3.metric("VaR (5%)", metrics["var_5"])