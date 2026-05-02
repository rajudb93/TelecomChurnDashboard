<<<<<<< HEAD
# 📊 Telecom Churn Intelligence Platform

A comprehensive Streamlit-based dashboard for analyzing and predicting telecom customer churn using machine learning, with integrated data visualization and automated recommendation systems.

## 🚀 Features

- **Interactive Dashboard**: Real-time KPIs, geographic distribution maps, and churn analysis visualizations
- **Churn Prediction**: Machine learning-powered prediction with XGBoost classifier
- **Automated Recommendations**: AI-driven retention strategies based on prediction results
- **Email Integration**: Automated email notifications with personalized recommendations
- **Snowflake Integration**: Direct connection to Snowflake data warehouse for real-time data access
- **Multi-page Application**: Organized navigation between dashboard and prediction interfaces

## 🛠 Tech Stack

### Frontend & UI
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation and analysis

### Backend & ML
- **Python**: Core programming language
- **XGBoost**: Machine learning model for churn prediction
- **Scikit-learn**: Data preprocessing and scaling
- **Joblib**: Model serialization

### Data & Infrastructure
- **Snowflake**: Cloud data warehouse
- **Snowflake Connector**: Python connector for Snowflake
- **SMTP**: Email sending via Gmail

### Additional Libraries
- **Geopandas/Shapely**: Geographic data processing
- **SHAP**: Model interpretability (potential future use)

## 🏗 Architecture

### High-Level Design (HLD)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Layer    │    │   ML Layer      │    │   UI Layer      │
│                 │    │                 │    │                 │
│ • Snowflake DB  │◄──►│ • XGBoost Model │◄──►│ • Streamlit App │
│ • Raw Data      │    │ • Preprocessing │    │ • Dashboard     │
│ • ETL Process   │    │ • Prediction    │    │ • Prediction    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Business Layer  │
                       │                 │
                       │ • Recommendations│
                       │ • Email Service  │
                       └─────────────────┘
```

#### Components Overview:
1. **Data Layer**: Handles data ingestion from Snowflake, including customer demographics, service usage, and churn labels
2. **ML Layer**: Processes input features, applies scaling, and generates churn probability predictions
3. **UI Layer**: Provides interactive web interface for data exploration and prediction input
4. **Business Layer**: Generates retention recommendations and handles email communications

### Low-Level Design (LLD)

#### Data Flow Architecture
```
Raw Data (Snowflake) → Data Loader → Preprocessing → ML Model → Prediction → Recommendations → Email
```

#### Module Breakdown:

**1. Data Layer (`src/snowflake/`)**
- `connection.py`: Establishes secure connection to Snowflake using credentials
- `loader.py`: Executes SQL queries and loads data into Pandas DataFrames

**2. ML Layer (`src/models/`)**
- `train.py`: Data preprocessing, feature engineering, model training, and serialization
- `predict.py`: Model loading, input preprocessing, and prediction generation

**3. Business Layer (`src/business/`)**
- `recommend.py`: Rule-based recommendation engine for customer retention
- `email_sender.py`: SMTP client for sending personalized email notifications

**4. UI Layer (`pages/`)**
- `1_Dashboard.py`: KPI metrics, geographic visualizations, and data exploration
- `2_Prediction.py`: User input forms, prediction display, and email integration
- `Advance_Viz.py`: Additional advanced visualizations

**5. Configuration**
- `.streamlit/secrets.toml`: Secure storage of sensitive credentials (email, Snowflake)
- `requirements.txt`: Python dependencies with versions

## 📋 Prerequisites

- Python 3.8+
- Google Account with 2FA enabled (for email functionality)
- Snowflake account with appropriate database access
- Virtual environment (recommended)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd telecom_churn_dashboard
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Secrets
Create `.streamlit/secrets.toml` in the project root:
```toml
# Email Configuration
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-16-char-app-password"

# Snowflake Configuration (if using)
SNOWFLAKE_USER = "your-snowflake-user"
SNOWFLAKE_PASSWORD = "your-snowflake-password"
SNOWFLAKE_ACCOUNT = "your-account-url"
SNOWFLAKE_WAREHOUSE = "your-warehouse"
SNOWFLAKE_DATABASE = "your-database"
SNOWFLAKE_SCHEMA = "your-schema"
```

### 5. Set Up Gmail App Password
1. Enable 2FA on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate password for "Mail" → "Other"
4. Use the 16-character password in `secrets.toml`

### 6. Train the Model (if needed)
```bash
python src/models/train.py
```

## 🚀 Usage

### Running the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Navigation
- **Home**: Overview and navigation guide
- **Dashboard**: Comprehensive data analysis and visualizations
- **Prediction**: Individual customer churn prediction with recommendations

### Using the Prediction Feature
1. Navigate to the Prediction page
2. Enter customer details (tenure, charges, contract type, etc.)
3. Click "Predict Churn"
4. View prediction results and recommendations
5. Optionally send results via email

## 📁 Project Structure

```
telecom_churn_dashboard/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
│
├── .streamlit/
│   └── secrets.toml               # Configuration secrets
│
├── data/
│   ├── customer_churn.csv         # Sample dataset
│   └── metadata.txt               # Data documentation
│
├── models/
│   ├── churn_model.pkl            # Trained XGBoost model
│   ├── scaler.pkl                 # Feature scaler
│   └── feature_columns.pkl        # Feature column names
│
├── pages/
│   ├── 1_Dashboard.py             # Main dashboard page
│   ├── 2_Prediction.py            # Prediction interface
│   └── Advance_Viz.py             # Advanced visualizations
│
├── src/
│   ├── business/
│   │   ├── email_sender.py        # Email functionality
│   │   └── recommend.py           # Recommendation engine
│   ├── models/
│   │   ├── predict.py             # Prediction logic
│   │   └── train.py               # Model training
│   └── snowflake/
│       ├── connection.py          # Snowflake connection
│       └── loader.py              # Data loading
│
└── temp/
    └── testing.ipynb              # Jupyter notebook for testing
```
=======
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
>>>>>>> cc46929a68ea0fc5f07b7400ef3fab24b19199d0

## 🔍 How It Works

### Data Pipeline
<<<<<<< HEAD
1. **Data Ingestion**: Customer data is loaded from Snowflake or local CSV files
2. **Preprocessing**: Features are encoded, scaled, and prepared for ML
3. **Model Training**: XGBoost classifier is trained on historical churn data
4. **Prediction**: User inputs are processed and fed into the trained model
5. **Recommendation**: Business rules generate retention strategies
6. **Communication**: Results are displayed and can be emailed to stakeholders

### Machine Learning Process
- **Features**: Tenure, monthly charges, total charges, contract type, internet service, payment method, tech support
- **Target**: Binary churn prediction (0/1)
- **Model**: XGBoost with optimized hyperparameters for imbalanced classification
- **Evaluation**: ROC-AUC, precision, recall, F1-score

### Business Logic
- **Churn Probability**: Ranges from 0-100%
- **Risk Levels**: Low (<30%), Medium (30-70%), High (>70%)
- **Recommendations**: Tailored retention strategies based on customer profile and risk level

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or issues:
- Check the [Issues](issues) section
- Review the code documentation
- Ensure all dependencies are properly installed

## 🔄 Future Enhancements

- [ ] Real-time data streaming from Snowflake
- [ ] Advanced ML models (Neural Networks, Ensemble methods)
- [ ] Customer segmentation clustering
- [ ] Automated retraining pipelines
- [ ] API endpoints for external integrations
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Advanced SHAP explanations for predictions</content>
<parameter name="filePath">e:\Learning\Python\telecom_churn_dashboard\telecom_churn_dashboard\README.md
=======
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

>>>>>>> cc46929a68ea0fc5f07b7400ef3fab24b19199d0
