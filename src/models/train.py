import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

df = pd.read_csv("data/customer_churn.csv")

df.columns = df.columns.str.strip()

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.fillna(0, inplace=True)

df['ChurnLabel'] = df['ChurnLabel'].map({'Yes': 1, 'No': 0})

FEATURES = [
    "TenureMonths",
    "MonthlyCharges",
    "TotalCharges",
    "Contract",
    "InternetService",
    "PaymentMethod",
    "TechSupport"
]

df = df[FEATURES + ["ChurnLabel"]]

df = pd.get_dummies(df, drop_first=True)

X = df.drop("ChurnLabel", axis=1)
y = df["ChurnLabel"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    scale_pos_weight=3,
    random_state=42
)

model.fit(X_train_scaled, y_train)

preds = model.predict(X_test_scaled)

print(classification_report(y_test, preds))
print("ROC AUC:", roc_auc_score(y_test, preds))

joblib.dump(model, "models/churn_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(X.columns.tolist(), "models/feature_columns.pkl")

print("✅ Model trained & saved")