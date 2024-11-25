import os
from dotenv import load_dotenv
import psutil
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading
import logging
import sys

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Exception handling decorator
def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return None
    return wrapper

@exception_handler
def check_disk_usage():
    usage = psutil.disk_usage('/')
    report = (f"Disk Usage:\n"
              f"Total: {usage.total / (1024 ** 3):.2f} GB\n"
              f"Used: {usage.used / (1024 ** 3):.2f} GB\n"
              f"Free: {usage.free / (1024 ** 3):.2f} GB\n"
              f"Percentage Used: {usage.percent}%")
    print(report)
    return report

@exception_handler
def monitor_services():
    result = subprocess.run(["systemctl", "list-units", "--type=service", "--state=running"], 
                             stdout=subprocess.PIPE, text=True)
    services = result.stdout
    print("Running Services:\n", services)
    return services

@exception_handler
def assess_memory_usage():
    memory = psutil.virtual_memory()
    report = (f"Memory Usage:\n"
              f"Total: {memory.total / (1024 ** 3):.2f} GB\n"
              f"Available: {memory.available / (1024 ** 3):.2f} GB\n"
              f"Used: {memory.used / (1024 ** 3):.2f} GB\n"
              f"Percentage Used: {memory.percent}%")
    print(report)
    return report

@exception_handler
def evaluate_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    report = f"CPU Usage: {cpu_percent}%"
    print(report)
    return report

# Fetch sensitive data from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))  # Default to 465
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


@exception_handler
def send_email_report(subject, content):
    message = MIMEMultipart()
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER
    message["Subject"] = subject
    message.attach(MIMEText(content, "plain"))

    try:
        # Use SMTP_SSL for port 465
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

@exception_handler
def generate_report():
    report = "\n".join([
        check_disk_usage(),
        assess_memory_usage(),
        evaluate_cpu_usage(),
        monitor_services()
    ])
    send_email_report("System Health Report", report)

@exception_handler
def schedule_email_reports():
    while True:
        generate_report()
        time.sleep(4 * 3600)  # Wait 4 hours

# Modify the menu to handle threading without breaking the loop
@exception_handler
def handle_option_5():
    if not hasattr(handle_option_5, "thread"):
        handle_option_5.thread = threading.Thread(target=schedule_email_reports, daemon=True)
        handle_option_5.thread.start()
        print("Started sending reports every four hours...")
    else:
        print("Reports are already scheduled.")

def main_menu():
    print("""
    System Health Check Menu
    1. Check Disk Usage
    2. Monitor Running Services
    3. Assess Memory Usage
    4. Evaluate CPU Usage
    5. Start Sending Reports Every Four Hours
    6. Exit
    """)

@exception_handler
def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            check_disk_usage()
        elif choice == "2":
            monitor_services()
        elif choice == "3":
            assess_memory_usage()
        elif choice == "4":
            evaluate_cpu_usage()
        elif choice == "5":
            handle_option_5()  # Use the updated function for Option 5
        elif choice == "6":
            print("Exiting the script.")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
