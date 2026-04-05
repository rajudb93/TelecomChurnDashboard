import streamlit as st
import plotly.express as px
import pandas as pd

from src.snowflake.loader import load_data

# ================= LOAD DATA =================
df = load_data()

st.title("📊 Telecom Customer Churn Dashboard")

# ================= KPI =================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", len(df))
col2.metric("Churn Rate", f"{df['ChurnValue'].mean()*100:.2f}%")
col3.metric("Avg Monthly Charges", f"{df['MonthlyCharges'].mean():.2f}")
col4.metric("Avg CLTV", f"{df['CLTV'].mean():.0f}")

st.divider()

# ================= GEO MAP (FIXED) =================
st.subheader("🌍 Geographic Distribution")

geo_df = df.copy()

# Split LatLong column
geo_split = geo_df['LatLong'].astype(str).str.replace(" ", "").str.split(",", expand=True)

geo_df["Latitude"] = pd.to_numeric(geo_split[0], errors="coerce")
geo_df["Longitude"] = pd.to_numeric(geo_split[1], errors="coerce")

# Clean data
geo_df = geo_df.dropna(subset=["Latitude", "Longitude"])

geo_df = geo_df[
    (geo_df["Latitude"].between(-90, 90)) &
    (geo_df["Longitude"].between(-180, 180))
]

st.caption(f"Valid geo points: {len(geo_df)}")

# Map (stable version)
fig_geo = px.scatter_geo(
    geo_df,
    lat="Latitude",
    lon="Longitude",
    color="ChurnValue",
    size="MonthlyCharges",
    hover_name="City",
    hover_data=["State", "Contract", "ChurnLabel"]
)

fig_geo.update_geos(
    projection_type="natural earth",
    showland=True,
    landcolor="lightgray"
)

st.plotly_chart(fig_geo, width='stretch', key="geo_map")

# ================= CATEGORICAL =================
st.subheader("📌 Categorical Analysis")

cat_cols = [
    'Gender', 'SeniorCitizen', 'Partner', 'Dependents',
    'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod'
]

selected_cat = st.selectbox("Select Feature", cat_cols)

fig_cat = px.histogram(df, x=selected_cat, color="ChurnLabel")

st.plotly_chart(fig_cat, width='stretch', key="cat_plot")

# ================= NUMERICAL =================
st.subheader("📈 Numerical Analysis")

num_cols = [
    "TenureMonths", "MonthlyCharges", "TotalCharges",
    "CLTV", "ChurnScore"
]

selected_num = st.selectbox("Select Numerical Feature", num_cols)

fig_num = px.box(df, x="ChurnLabel", y=selected_num)

st.plotly_chart(fig_num, width='stretch', key="num_plot")

# ================= CONTRACT =================
st.subheader("📄 Contract Impact")

fig_contract = px.histogram(df, x="Contract", color="ChurnLabel")

st.plotly_chart(fig_contract, width='stretch', key="contract_plot")

# ================= PAYMENT =================
st.subheader("💳 Payment Behavior")

fig_payment = px.histogram(df, x="PaymentMethod", color="ChurnLabel")

st.plotly_chart(fig_payment, width='stretch', key="payment_plot")

# ================= TENURE =================
st.subheader("⏳ Tenure Analysis")

df['TenureGroup'] = pd.cut(df['TenureMonths'], bins=5).astype(str)

tenure_df = df.groupby('TenureGroup', observed=False)['ChurnValue'].mean().reset_index()

fig_tenure = px.bar(
    tenure_df,
    x="TenureGroup",
    y="ChurnValue",
    title="Churn Rate by Tenure Group"
)

st.plotly_chart(fig_tenure, width='stretch', key="tenure_plot")

# ================= SERVICES =================
st.subheader("📡 Services Impact")

service_cols = [
    "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies"
]

selected_service = st.selectbox("Select Service", service_cols)

fig_service = px.histogram(df, x=selected_service, color="ChurnLabel")

st.plotly_chart(fig_service, width='stretch', key="service_plot")

# ================= CHURN REASON =================
st.subheader("❗ Churn Reasons")

reason_df = df[df['ChurnLabel'] == "Yes"]

fig_reason = px.histogram(reason_df, x="ChurnReason")

st.plotly_chart(fig_reason, width='stretch', key="reason_plot")

st.divider()
st.header("📊 Advanced Data Insights")

# ================= NUMERIC COLUMNS =================
num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Remove target leakage columns if needed
exclude_cols = ["ChurnValue"]
num_cols = [col for col in num_cols if col not in exclude_cols]

# ================= 1. HISTOGRAM =================
st.subheader("📈 Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    hist_col = st.selectbox("Select column (Histogram)", num_cols, key="hist")

    fig_hist = px.histogram(
        df,
        x=hist_col,
        marginal="box",
        title=f"Distribution of {hist_col}"
    )

    st.plotly_chart(fig_hist, width='stretch', key="hist_plot")

with col2:
    box_col = st.selectbox("Select column (Box Plot)", num_cols, key="box")

    fig_box = px.box(
        df,
        y=box_col,
        color="ChurnLabel",
        title=f"{box_col} Distribution by Churn"
    )

    st.plotly_chart(fig_box, width='stretch', key="box_plot")

# ================= 2. SCATTER RELATION =================
st.subheader("🔗 Feature Relationships")

col3, col4 = st.columns(2)

with col3:
    x_col = st.selectbox("X-axis", num_cols, key="scatter_x")
    y_col = st.selectbox("Y-axis", num_cols, key="scatter_y")

    if x_col != y_col:
        fig_scatter = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color="ChurnLabel",
            trendline="ols",
            title=f"{x_col} vs {y_col}"
        )

        st.plotly_chart(fig_scatter, width='stretch', key="scatter_plot")
    
    else:
        st.error("Select different columns")

with col4:
    fig_density = px.density_heatmap(
        df,
        x=x_col,
        y=y_col,
        title="2D Density Heatmap"
    )

    st.plotly_chart(fig_density, width='stretch', key="heatmap_plot")

# ================= 3. CORRELATION =================
st.subheader("🔥 Correlation Heatmap")

corr = df[num_cols].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation Matrix"
)

st.plotly_chart(fig_corr, width='stretch', key="corr_plot")


# ================= 4. VIOLIN PLOT =================
st.subheader("🎻 Distribution Comparison")

violin_col = st.selectbox("Select column (Violin)", num_cols, key="violin")

fig_violin = px.violin(
    df,
    y=violin_col,
    x="ChurnLabel",
    box=True,
    points="all"
)

st.plotly_chart(fig_violin, width='stretch', key="violin_plot")

# ================= 5. PAIR PLOT (SCATTER MATRIX) =================
st.subheader("🧠 Multi-variable Analysis")

selected_features = st.multiselect(
    "Select features for scatter matrix",
    num_cols,
    default=num_cols[:4]
)

if len(selected_features) >= 2:
    fig_matrix = px.scatter_matrix(
        df,
        dimensions=selected_features,
        color="ChurnLabel"
    )

    st.plotly_chart(fig_matrix, width='stretch', key="matrix_plot")

# ================= 6. STRIP / JITTER =================
st.subheader("📍 Detailed Distribution (Strip Plot)")

strip_col = st.selectbox("Select column (Strip)", num_cols, key="strip")

fig_strip = px.strip(
    df,
    x="ChurnLabel",
    y=strip_col,
    color="ChurnLabel"
)

st.plotly_chart(fig_strip, width='stretch', key="strip_plot")