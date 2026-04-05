import joblib
import pandas as pd
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

model = joblib.load("models/churn_model.pkl")
scaler = joblib.load("models/scaler.pkl")
FEATURE_COLUMNS = joblib.load("models/feature_columns.pkl")

def predict_churn(input_dict):
    df = pd.DataFrame([input_dict])

    df = pd.get_dummies(df)

    df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)

    df_scaled = scaler.transform(df)

    prob = model.predict_proba(df_scaled)[0][1]

    return prob