import ssl
import smtplib
from email.message import EmailMessage

class EmailSender:
    def __init__(self, email_sender, password_sender, email_receiver):
        self.email_sender = email_sender
        self.password_sender = password_sender
        self.email_receiver = email_receiver

    def send_email(self, subject, body):
        em = EmailMessage()
        em['From'] = self.email_sender
        em['To'] = self.email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.password_sender)
            smtp.sendmail(self.email_sender, self.email_receiver, em.as_string())


