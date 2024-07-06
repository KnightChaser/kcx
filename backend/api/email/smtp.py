# backend/api/email/smtp.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from rich.console import Console

class SMTP:
    def __init__(self):
        email_secret_file_absolute_path = os.path.join(os.path.dirname(__file__), '..', '..', '.secrets.smtp')
        load_dotenv(email_secret_file_absolute_path)
        self.smtp_server_username = os.getenv('SMTP_USERNAME')
        self.smtp_server_password = os.getenv('SMTP_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))

        if not self.smtp_server_username or not self.smtp_server_password:
            raise Exception('SMTP server username and password not found in .secrets.smtp file')
        
        self.sender_email = "no_reply@kcx.knightchaser.com"
        self.console = Console()

    def send_email(self, receiver_email, subject, body, purpose = None):
        """
        Send an email using the preregistered SMTP server
        """
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            # Set up the server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(self.smtp_server_username, self.smtp_server_password)  # Login

            # Send the email
            server.sendmail(from_addr=self.sender_email, to_addrs=receiver_email, msg=msg.as_string())
            self.console.print(f"Email sent to {receiver_email} for {purpose} successfully")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()  # Terminate the SMTP session

