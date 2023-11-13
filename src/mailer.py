import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import openai


def get_solution(description):
    openai.api_key = "your-openai-api-key"
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Describe a problem and propose a detailed solution:\n\nProblem: {description}\n\nSolution:",
        max_tokens=150,
    )
    return response.choices[0].text.strip()


# Email credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


# Send email function
def send_email(subject, body, recipient):
    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(message)
