import streamlit as st
import plotly.graph_objects as go
from src.models.predict import predict_churn
from src.business.recommend import recommend_action 
from src.business.email_sender import send_email 


st.title("🎯 Predict Customer Churn")

# ================= INPUT =================
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("TenureMonths", 0, 72)
    monthly = st.number_input("MonthlyCharges", 0.0, 200.0)
    total = st.number_input("TotalCharges", 0.0, 10000.0)

with col2:
    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    internet = st.selectbox(
        "InternetService",
        ["DSL", "Fiber optic", "No"]
    )

    payment = st.selectbox(
        "PaymentMethod",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    tech = st.selectbox(
        "TechSupport",
        ["Yes", "No"]
    )

# ================= PREDICT (with session state) =================
# initialize session state keys
if 'predict_clicked' not in st.session_state:
    st.session_state.predict_clicked = False
if 'send_clicked' not in st.session_state:
    st.session_state.send_clicked = False
if 'prob' not in st.session_state:
    st.session_state.prob = None
if 'result' not in st.session_state:
    st.session_state.result = None
if 'email_response' not in st.session_state:
    st.session_state.email_response = None

# keep customer inputs in session_state so callbacks/reruns can access them
customer_name = st.text_input("Enter name of customer", key="customer_name")
user_email = st.text_input("Enter customer email", key="user_email")

# buttons update session state instead of performing actions directly
if st.button("Predict Churn", key="predict_btn"):
    st.session_state.predict_clicked = True
    st.session_state.email_response = None  # clear previous email response

# perform prediction when flag is set
if st.session_state.predict_clicked:
    input_data = {
        "TenureMonths": tenure,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
        "Contract": contract,
        "InternetService": internet,
        "PaymentMethod": payment,
        "TechSupport": tech
    }
    prob = predict_churn(input_data)
    st.session_state.prob = prob
    st.session_state.result = recommend_action(prob, customer_name=customer_name or "")

    st.write(f"### Churn Probability: {prob:.2f}")

    # ================= COLOR LOGIC =================
    if prob <= 0.4:
        color = "green"
        label = "✅ Low Risk"
        st.success(label)

    elif prob <= 0.7:
        color = "orange"
        label = "⚠️ Medium Risk"
        st.warning(label)

    else:
        color = "red"
        label = "🚨 High Risk"
        st.error(label)

    # ================= GAUGE =================
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={'text': "Churn Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color}
        }
    ))

    st.plotly_chart(fig, width='stretch', key="gauge_chart")

# Send email button sets a flag; actual sending happens when flag processed
if st.button("Send Email", key="send_btn"):
    st.session_state.send_clicked = True

if st.session_state.send_clicked:
    if st.session_state.result is None:
        st.warning("Please run prediction before sending an email.")
    elif not user_email:
        st.warning("Please provide a customer email address.")
    else:
        response = send_email(
            to_email=user_email,
            subject=st.session_state.result["subject"],
            message=st.session_state.result["message"]
        )
        st.session_state.email_response = response

    # reset send flag so subsequent clicks will trigger again
    st.session_state.send_clicked = False

# show email response if available
if st.session_state.email_response:
    st.info(st.session_state.email_response)