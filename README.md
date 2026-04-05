📊 Telecom Customer Churn Intelligence SystemAn end-to-end Predictive Analytics and Automated Retention platform. This system utilizes XGBoost to identify at-risk customers, Snowflake for scalable data warehousing, and Streamlit for a high-performance business interface.🚀 Project OverviewChurn is the "silent killer" of telecom revenue. This project transforms raw subscriber data into proactive business outcomes. Instead of simply reporting who left last month, this system predicts who will leave next month and provides the tools to stop it.Core Capabilities:Executive Dashboard: High-level KPIs (Churn Rate, CLTV) and geographic hotspots.AI-Powered Predictions: Individual risk scoring using a tuned XGBoost Classifier.Explainable AI (XAI): Visualizing "Why" a customer is at risk (via SHAP values).Automated Retention: A business rules engine that generates personalized recovery offers.Closed-Loop Outreach: Integrated SMTP system to send retention emails directly from the UI.🛠️ Tech StackCategoryToolsFrontend/UIStreamlit, Plotly (Express & Graph Objects)Data ScienceXGBoost, Scikit-learn, Pandas, NumPyDatabaseSnowflake (Snowflake-connector-python)ExplainabilitySHAPGeospatialGeoPandas, ShapelySecurityPython-dotenv, Streamlit SecretsDevOpsJoblib (Model Serialization)🏗️ Architecture (HLD & LLD)High-Level Design (HLD)The system is divided into four distinct layers that interact via a "Push-Pull" data flow:Data Layer: Managed Snowflake connection with local CSV failover.ML Layer: Handles feature engineering, scaling, and XGBoost inference.Business Layer: Maps model probabilities to retention strategies.UI Layer: Responsive multi-page Streamlit application.Low-Level Design (LLD)src/snowflake/loader.py: Implements @st.cache_data to minimize warehouse costs and provides the try-except failover logic.src/models/predict.py: Loads scaler.pkl and churn_model.pkl to transform raw JSON input into a model-ready tensor.src/business/recommend.py: A logic-gate system that segments customers into High, Medium, and Low risk buckets.src/business/email_sender.py: Manages secure SMTP handshake and MIME multi-part email construction.📂 Project StructurePlaintextTELECOM_CHURN_DASHBOARD/
├── .streamlit/
│   └── secrets.toml          # Snowflake & SMTP Credentials
├── data/
│   └── customer_churn.csv    # Local fallback dataset
├── models/
│   ├── churn_model.pkl       # Serialized XGBoost model
│   └── scaler.pkl            # Trained StandardScaler
├── pages/
│   ├── 1_Dashboard.py        # EDA & Interactive Charts
│   ├── 2_Prediction.py       # ML Inference & Email trigger
│   └── Advance_Viz.py        # SHAP & Geospatial deep-dives
├── src/
│   ├── business/             # email_sender.py, recommend.py
│   ├── models/               # predict.py, train.py
│   └── snowflake/            # connection.py, loader.py
├── app.py                    # App Entry Point & Sidebar
└── requirements.txt          # Python dependencies
⚙️ Installation & Setup1. Environment SetupBashgit clone <repository-url>
cd TELECOM_CHURN_DASHBOARD
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
2. Configuration (secrets.toml)Create .streamlit/secrets.toml to store sensitive data:Ini, TOMLEMAIL_USER = "marketing@telecom.com"
EMAIL_PASSWORD = "your-16-digit-app-password"

[snowflake]
user = "..."
password = "..."
account = "..."
warehouse = "..."
database = "..."
schema = "..."
🔍 How It WorksThe Data PipelineThe app uses a Hybrid Loader. It first checks for a live Snowflake session. If valid, it pulls the latest CUSTOMER_CHURN records. Data is cached for 600 seconds to ensure the UI remains snappy during filter changes.The ML ProcessInput: User selects features (Tenure, Contract, etc.) in the UI.Transformation: Input is passed through the saved scaler.pkl.Inference: XGBClassifier calculates the churn probability ($P$).Thresholding:$P > 0.7$: High Risk (Red Label)$0.4 < P \le 0.7$: Medium Risk (Orange Label)$P \le 0.4$: Low Risk (Green Label)The Business LogicBased on the threshold, the app fetches a pre-defined email template from recommend.py. The user can then click "Send Email", which triggers the smtplib module to dispatch the offer to the customer.🏃 UsageRun the application from the root directory:Bashstreamlit run app.py
Navigate via the sidebar.Dashboard: Use filters to identify churn trends by Payment Method.Prediction: Input a customer ID or manual stats to see real-time risk.🔮 Future PlansModel Monitoring: Track prediction accuracy over time as new data arrives from Snowflake.Automated Retraining: Implement a monthly GitHub Action to retrain on combined historical/new data.LLM Integration: Use Gemini/OpenAI to generate even more personalized email content based on SHAP explanation values.
