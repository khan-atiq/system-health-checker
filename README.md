
# Menu-Driven Health Check
This project is a Python-based script for performing system health checks, such as monitoring disk usage, running services, memory usage, and CPU usage. The tool also sends automated reports via email.

Table of Contents
Project Setup
Running the Script
Rewriting Git History
Contributing
License
Project Setup
Prerequisites
Python 3.x
Git
SMTP Configuration (via .env file for email credentials)
Steps to Setup
Clone the repository:

bash git clone https://github.com/khan-atiq/system-health-checker.git

Install dependencies:

bash pip install -r requirements.txt
Set up the .env file with your SMTP server configuration:

env

SMTP_SERVER=smtp.yourserver.com
SMTP_PORT=465
SENDER_EMAIL=your-email@example.com
PASSWORD=your-email-password
RECEIVER_EMAIL=receiver-email@example.com
Run the system health check script:

bash python sys_healthCheck.py
Running the Script
After setting up the .env file, execute the script:


The script will present you with a menu of options:

Check Disk Usage
Monitor Running Services
Assess Memory Usage
Evaluate CPU Usage
Send a Comprehensive Report via Email (every 4 hours)
Select an option by entering the corresponding number.
