import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:

    def __init__(self, smtp_server, sender_email, password, port=465):
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.password = password
        self.port = port

    def send(self, receiver_email, subject,  text_message):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message.attach(MIMEText(text_message, "plain"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())


if __name__ == "__main__":
    smtp_server = "smtp.gmail.com"
    sender_email = "mark.grengoric@gmail.com"  # Enter your address
    receiver_email = "mateusz.koniuszewski@gmail.com"  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """\
    This message is sent from Python."""
    sender = EmailSender(smtp_server, sender_email, password)
    sender.send(receiver_email, "Hi there", message)
