import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL

def send_email_alert(sensor_id, current, avg, z_score):
    subject = f"🚨 ALERT: {sensor_id} Critical Temperature"

    body = f"""
    ALERT TRIGGERED!

    Sensor: {sensor_id}
    Current Temp: {current}
    Moving Avg: {avg}
    Z-Score: {z_score}

    Action Required!
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("[EMAIL] Alert sent successfully")

    except Exception as e:
        print("[EMAIL ERROR]", e)