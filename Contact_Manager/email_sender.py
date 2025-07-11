
import smtplib
from email.message import EmailMessage

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, str(e)
