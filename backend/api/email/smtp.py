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

    def send_email(self, receiver_email, subject, body, purpose=None):
        """
        Send an email using the preregistered SMTP server
        """
        # Create the email
        msg = MIMEMultipart("alternative")
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add both plain text and HTML versions
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(self.create_html_body(body), 'html')

        msg.attach(part1)
        msg.attach(part2)

        try:
            # Set up the server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(self.smtp_server_username, self.smtp_server_password)  # Login

            # Send the email
            server.sendmail(from_addr=self.sender_email, to_addrs=receiver_email, msg=msg.as_string())
            self.console.print(f"Email sent to {receiver_email} for {purpose} successfully")
        except Exception as e:
            self.console.print(f"Error: {e}")
        finally:
            server.quit()  # Terminate the SMTP session

    def create_html_body(self, body):
        """
        Create an HTML version of the email body.
        This is used to send emails with rich text formatting.
        """
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                <h2 style="color: #333;">KCX Email Verification</h2>
                <p style="color: #555;">Thank you for using KCX. Please use the following code to verify your email address:</p>
                <h3 style="color: #333; background-color: #f7f7f7; padding: 10px; border-radius: 5px; display: inline-block;">{body.split(": ")[1]}</h3>
                <p style="color: #555;">If you did not request this verification, please ignore this email.</p>
                <p style="color: #555;">Best regards, <br>KnightChaser</p>.
            </div>
        </body>
        </html>
        """
        return html
