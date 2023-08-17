from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Twilio credentials
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
twilio_phone_number = 'your_twilio_phone_number'

client = Client(account_sid, auth_token)

def send_sms(recipient, message):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=recipient
    )

def send_whatsapp(recipient, message):
    client.messages.create(
        body=message,
        from_='whatsapp:'+twilio_phone_number,
        to='whatsapp:'+recipient
    )

# Email credentials
smtp_server = 'your_smtp_server'
smtp_port = 'your_smtp_port'
email_user = 'your_email_user'
email_password = 'your_email_password'

def send_email(recipient, message):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient
    msg['Subject'] = 'Notification'
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_user, email_password)
    text = msg.as_string()
    server.sendmail(email_user, recipient, text)
    server.quit()
