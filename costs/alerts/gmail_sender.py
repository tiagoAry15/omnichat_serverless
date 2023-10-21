import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv


def send_gmail(subject, body, to_email, gmail_user, gmail_password):
    # Create the message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    # Connect to the Gmail server
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, [to_email], msg.as_string())
        server.close()
        print('Email sent!')
    except Exception as e:
        print('Failed to send email:', e)


def __main():
    # Usage
    load_dotenv()
    gmail_user = os.environ['SEND_GMAIL_USERNAME']
    gmail_password = os.environ['SEND_GMAIL_APP_PASSWORD']

    send_gmail(
        subject='Test Email',
        body='This is a test email sent from Python.',
        to_email='matbessa12@gmail.com',  # Replace with the recipient's email address
        gmail_user=gmail_user,
        gmail_password=gmail_password
    )


if __name__ == '__main__':
    __main()
