# 📊 Telecom Customer Churn Intelligence System

> An end-to-end Predictive Analytics and Automated Retention platform — powered by XGBoost, Snowflake, and Streamlit.

---

## 🚀 Overview

Churn is the **silent killer** of telecom revenue. This system transforms raw subscriber data into proactive business outcomes — predicting *who will leave next month* and equipping teams with the tools to stop it.

### Core Capabilities

- **Executive Dashboard** — High-level KPIs (Churn Rate, CLTV) with geographic hotspot visualization
- **AI-Powered Predictions** — Individual customer risk scoring via a tuned XGBoost Classifier
- **Explainable AI (XAI)** — SHAP-based visualization of *why* a customer is flagged as at-risk
- **Automated Retention Engine** — Business rules that generate personalized recovery offers
- **Closed-Loop Outreach** — Send retention emails directly from the UI via integrated SMTP

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Frontend / UI | Streamlit, Plotly (Express & Graph Objects) |
| Data Science | XGBoost, Scikit-learn, Pandas, NumPy |
| Database | Snowflake (`snowflake-connector-python`) |
| Explainability | SHAP |
| Geospatial | GeoPandas, Shapely |
| Security | python-dotenv, Streamlit Secrets |
| DevOps | Joblib (Model Serialization) |

---

## 🏗️ Architecture

### High-Level Design (HLD)

Four distinct layers interact via a **Push-Pull** data flow:

1. **Data Layer** — Managed Snowflake connection with local CSV failover
2. **ML Layer** — Feature engineering, scaling, and XGBoost inference
3. **Business Layer** — Maps model probabilities to retention strategies
4. **UI Layer** — Responsive multi-page Streamlit application

### Low-Level Design (LLD)

| File | Responsibility |
|---|---|
| `src/snowflake/loader.py` | `@st.cache_data` for warehouse cost control + try/except CSV failover |
| `src/models/predict.py` | Loads `scaler.pkl` + `churn_model.pkl`; transforms raw input into model tensor |
| `src/business/recommend.py` | Logic-gate segmentation into High / Medium / Low risk buckets |
| `src/business/email_sender.py` | Secure SMTP handshake + MIME multi-part email construction |

---

## 📂 Project Structure
TELECOM_CHURN_DASHBOARD/
├── .streamlit/
│   └── secrets.toml          # Snowflake & SMTP credentials
├── data/
│   └── customer_churn.csv    # Local fallback dataset
├── models/
│   ├── churn_model.pkl       # Serialized XGBoost model
│   └── scaler.pkl            # Trained StandardScaler
├── pages/
│   ├── 1_Dashboard.py        # EDA & interactive charts
│   ├── 2_Prediction.py       # ML inference & email trigger
│   └── Advance_Viz.py        # SHAP & geospatial deep-dives
├── src/
│   ├── business/             # email_sender.py, recommend.py
│   ├── models/               # predict.py, train.py
│   └── snowflake/            # connection.py, loader.py
├── app.py                    # App entry point & sidebar
└── requirements.txt

---

## ⚙️ Setup

### 1. Clone & Install
```bash
git clone <repository-url>
cd TELECOM_CHURN_DASHBOARD
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Credentials

Create `.streamlit/secrets.toml`:
```toml
EMAIL_USER = "marketing@telecom.com"
EMAIL_PASSWORD = "your-16-digit-app-password"

[snowflake]
user = "..."
password = "..."
account = "..."
warehouse = "..."
database = "..."
schema = "..."
```

---

## 🔍 How It Works

### Data Pipeline
The app uses a **Hybrid Loader** — it first attempts a live Snowflake connection to pull the latest `CUSTOMER_CHURN` records, then falls back to a local CSV if unavailable. Data is cached for 600 seconds to keep the UI responsive during filter changes.

### ML Inference Flow

1. **Input** — User selects features (Tenure, Contract Type, etc.) in the UI
2. **Transformation** — Input is passed through the saved `scaler.pkl`
3. **Inference** — XGBClassifier outputs a churn probability *P*
4. **Thresholding**:
   - 🔴 `P > 0.70` → **High Risk**
   - 🟠 `0.40 < P ≤ 0.70` → **Medium Risk**
   - 🟢 `P ≤ 0.40` → **Low Risk**

### Business Logic
Risk tier determines the email template fetched from `recommend.py`. One click sends a personalized retention offer via `smtplib`.

---

## 🏃 Usage
```bash
streamlit run app.py
```

| Page | What to do |
|---|---|
| **Dashboard** | Filter churn trends by Payment Method and region |
| **Prediction** | Input a Customer ID or manual stats for real-time risk scoring |
| **Advanced Viz** | Explore SHAP explanations and geospatial churn heatmaps |

---

## 🔮 Roadmap

- [ ] **Model Monitoring** — Track prediction accuracy drift as new Snowflake data arrives
- [ ] **Automated Retraining** — Monthly GitHub Action to retrain on cumulative historical data
- [ ] **LLM Integration** — Use Gemini / OpenAI to generate hyper-personalized email content grounded in SHAP explanation values

