import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from src.snowflake.loader import load_data

# ML / Explainability
import shap
import joblib

# Clustering
from sklearn.cluster import KMeans

# ================= LOAD =================
df = load_data()

st.set_page_config(layout="wide")
st.title("📊 Telecom Churn Intelligence Platform")

# ================= TABS =================
tabs = st.tabs([
    "📊 Overview",
    "🌍 Geo",
    "📈 Features",
    "💳 Business",
    "📊 Advanced",
    "🧠 Relationships",
    "🔥 Correlation",
    "🤖 Explainability",
    "📊 Segmentation",
    "📈 Trends",
    "🔍 Drill Down"
])

# =========================================================
# 📊 OVERVIEW
# =========================================================
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customers", len(df))
    col2.metric("Churn Rate", f"{df['ChurnValue'].mean()*100:.2f}%")
    col3.metric("Avg Monthly Charges", f"{df['MonthlyCharges'].mean():.2f}")
    col4.metric("Avg CLTV", f"{df['CLTV'].mean():.0f}")

# =========================================================
# 🌍 GEO
# =========================================================
with tabs[1]:
    geo_df = df.copy()

    geo_split = geo_df['LatLong'].astype(str).str.replace(" ", "").str.split(",", expand=True)
    geo_df["Latitude"] = pd.to_numeric(geo_split[0], errors="coerce")
    geo_df["Longitude"] = pd.to_numeric(geo_split[1], errors="coerce")

    geo_df = geo_df.dropna(subset=["Latitude", "Longitude"])

    fig = px.scatter_geo(
        geo_df,
        lat="Latitude",
        lon="Longitude",
        color="ChurnValue",
        hover_name="City"
    )

    st.plotly_chart(fig, width='stretch', key="geo")

# =========================================================
# 📈 FEATURES
# =========================================================
with tabs[2]:
    cat = st.selectbox("Categorical", df.select_dtypes("object").columns)
    fig = px.histogram(df, x=cat, color="ChurnLabel")
    st.plotly_chart(fig, width='stretch', key="feat_cat")

    num = st.selectbox("Numerical", df.select_dtypes(["int64","float64"]).columns)
    fig = px.box(df, x="ChurnLabel", y=num)
    st.plotly_chart(fig, width='stretch', key="feat_num")

# =========================================================
# 💳 BUSINESS
# =========================================================
with tabs[3]:
    fig = px.histogram(df, x="PaymentMethod", color="ChurnLabel")
    st.plotly_chart(fig, width='stretch', key="payment")

    df['TenureGroup'] = pd.cut(df['TenureMonths'], bins=5).astype(str)
    tenure_df = df.groupby('TenureGroup')['ChurnValue'].mean().reset_index()
    fig = px.bar(tenure_df, x="TenureGroup", y="ChurnValue")
    st.plotly_chart(fig, width='stretch', key="tenure")

# =========================================================
# 📊 ADVANCED
# =========================================================
with tabs[4]:
    cols = df.select_dtypes(["int64","float64"]).columns

    x = st.selectbox("X", cols)
    y = st.selectbox("Y", cols)

    fig = px.scatter(df, x=x, y=y, color="ChurnLabel")
    st.plotly_chart(fig, width='stretch', key="scatter")

# =========================================================
# 🧠 RELATIONSHIPS
# =========================================================
with tabs[5]:
    fig = px.scatter_matrix(df, dimensions=df.select_dtypes(["int64","float64"]).columns[:4])
    st.plotly_chart(fig, width='stretch', key="matrix")

# =========================================================
# 🔥 CORRELATION
# =========================================================
with tabs[6]:
    corr = df.select_dtypes(["int64","float64"]).corr()
    fig = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig, width='stretch', key="corr")

# =========================================================
# 🤖 SHAP EXPLAINABILITY
# =========================================================
with tabs[7]:

    st.subheader("🤖 Explainability (Why Customer Churns)")

    try:
        import shap
        import joblib
        import matplotlib.pyplot as plt

        # ================= LOAD =================
        model = joblib.load("models/churn_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        FEATURE_COLUMNS = joblib.load("models/feature_columns.pkl")

        # ================= SELECT CUSTOMER =================
        sample = df.sample(5)

        st.write("Selected Customer")
        st.dataframe(sample)

        # ================= PREPROCESS =================
        input_df = sample[[
            "TenureMonths",
            "MonthlyCharges",
            "TotalCharges",
            "Contract",
            "InternetService",
            "PaymentMethod",
            "TechSupport"
        ]]

        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=FEATURE_COLUMNS, fill_value=0)

        input_scaled = scaler.transform(input_df)

        # ================= SHAP =================
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_scaled)

        # ================= BAR PLOT (FIXED) =================
        fig, ax = plt.subplots()

        shap.summary_plot(
            shap_values,
            input_scaled,
            feature_names=FEATURE_COLUMNS,
            plot_type="bar",
            show=False
        )

        st.pyplot(fig) 

        # ================= FORCE PLOT =================
        st.write("### 🎯 Individual Prediction Explanation")

        plt.figure(figsize=(10,8))

        force_plot = shap.force_plot(
            np.round(explainer.expected_value,2),
            np.round(shap_values[0],2),
            np.round(input_scaled[0],2),
            feature_names=FEATURE_COLUMNS,
            matplotlib=True
        )

        st.pyplot(plt.gcf())

    except Exception as e:
        st.error(f"SHAP Error: {str(e)}")

# =========================================================
# 📊 SEGMENTATION
# =========================================================
with tabs[8]:

    st.subheader("Customer Segmentation")

    features = ["TenureMonths", "MonthlyCharges", "TotalCharges"]

    seg_df = df[features].copy()

    # 🔥 FIX: Clean data properly
    for col in features:
        seg_df[col] = pd.to_numeric(seg_df[col], errors="coerce")

    seg_df = seg_df.fillna(0)

    # KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Segment"] = kmeans.fit_predict(seg_df)

    fig = px.scatter(
        df,
        x="MonthlyCharges",
        y="TenureMonths",
        color=df["Segment"].astype(str)
    )

    st.plotly_chart(fig, width='stretch', key="segment")

# =========================================================
# 📈 TREND FORECASTING
# =========================================================
with tabs[9]:
    st.subheader("Churn Trend")

    if "TenureMonths" in df.columns:
        trend = df.groupby("TenureMonths")["ChurnValue"].mean().reset_index()

        fig = px.line(trend, x="TenureMonths", y="ChurnValue")
        st.plotly_chart(fig, width='stretch', key="trend")

# =========================================================
# 🔍 DRILL DOWN
# =========================================================
with tabs[10]:

    st.subheader("State → City → Customer")

    state = st.selectbox("Select State", df["State"].unique())

    state_df = df[df["State"] == state]

    city = st.selectbox("Select City", state_df["City"].unique())

    city_df = state_df[state_df["City"] == city]

    st.write(f"Customers in {city}")

    st.dataframe(city_df.head(20))

    fig = px.histogram(city_df, x="ChurnLabel")
    st.plotly_chart(fig, width='stretch', key="drill")