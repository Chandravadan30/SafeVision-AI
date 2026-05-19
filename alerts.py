import cv2
import os
from datetime import datetime
from config import (
    SNAPSHOT_DIR, SENDGRID_API_KEY, ALERT_EMAIL_FROM, ALERT_EMAIL_TO,
    TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO
)
from logger import log_event

def save_snapshot(frame):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{SNAPSHOT_DIR}/fall_{ts}.jpg"
    cv2.imwrite(path, frame)
    print(f"[alerts] Snapshot saved: {path}")
    return path

def send_email(snapshot_path):
    if not SENDGRID_API_KEY or SENDGRID_API_KEY == "SG.xxx":
        print("[alerts] SendGrid not configured, skipping email")
        return
    try:
        import base64
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import (
            Mail, Attachment, FileContent, FileName, FileType
        )
        with open(snapshot_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        msg = Mail(
            from_email=ALERT_EMAIL_FROM,
            to_emails=ALERT_EMAIL_TO,
            subject="SafeVision AI: Fall Detected",
            html_content="<p>A fall was detected. Snapshot attached.</p>"
        )
        att = Attachment(
            FileContent(data),
            FileName("fall.jpg"),
            FileType("image/jpeg")
        )
        msg.attachment = att
        SendGridAPIClient(SENDGRID_API_KEY).send(msg)
        print("[alerts] Email sent successfully")
    except Exception as e:
        print(f"[alerts] Email failed: {e}")

def send_sms():
    if not TWILIO_SID or TWILIO_SID == "ACxxx":
        print("[alerts] Twilio not configured, skipping SMS")
        return
    try:
        from twilio.rest import Client
        Client(TWILIO_SID, TWILIO_TOKEN).messages.create(
            body="SafeVision AI: Fall detected! Check the dashboard.",
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print("[alerts] SMS sent successfully")
    except Exception as e:
        print(f"[alerts] SMS failed: {e}")

def trigger_alert(frame, angle):
    path = save_snapshot(frame)
    log_event("fall_detected", angle=angle, snapshot_path=path)
    send_email(path)
    send_sms()
    return path
