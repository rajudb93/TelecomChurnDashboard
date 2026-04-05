import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st 


def send_email(to_email, subject, message):
    
    # ================= CONFIG =================
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    EMAIL_USER = st.secrets["EMAIL_USER"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

    try:
        # ================= SETUP MESSAGE =================
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        # ================= CONNECT =================
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        # ================= SEND =================
        server.send_message(msg)
        server.quit()

        return "✅ Email sent successfully!"

    except Exception as e:
        return f"❌ Error: {str(e)}"