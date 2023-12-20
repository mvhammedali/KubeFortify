import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


def get_solution(description):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Describe a problem and propose a detailed solution:\n\nProblem: {description}\n\nSolution:",
        max_tokens=300,
    )
    return response.choices[0].text.strip()


# Send email function
def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = os.getenv("EMAIL_SENDER")
    message["To"] = os.getenv("EMAIL_RECEIVER")
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(
            host=os.getenv("EMAIL_HOST"), port=os.getenv("EMAIL_PORT"), timeout=10
        ) as server:  # Added timeout
            server.starttls()  # Secure the connection
            server.login(os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_PASSWORD"))
            server.send_message(message)
            print("Email has been sent!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
