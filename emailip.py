import smtplib
from email.mime.text import MIMEText
import requests
import time
import psutil


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving public IP: {e}")
        return None

def get_system_stats():
    """Get basic system stats."""
    stats = {
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
        "Memory Usage": f"{psutil.virtual_memory().percent}%",
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        "Uptime": f"{psutil.boot_time()}"
    }
    return stats

def send_email(ip):
    sender_email = "youremail@yourdomain.com"  # Replace with your email
    sender_password = "use an app password"  # Replace with your email password
    recipient_email = "email to send to"  # Replace with your email to receive notifications

    if not ip:
        print("No IP Address to Send.")
        return
    stats = get_system_stats()

    email_body = (f"Your HonmeLab Server:\n\nYour public IP address is: {ip}\n\nSystem Stats:\n")
    for key,value in stats.items():
        email_body += f"{key:} {value}\n"
    

    try:
        msg = MIMEText(email_body)
        msg['Subject'] = "Server Information"
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":

    last_sent_ip = None  
    email_interval = 3600  # Set interval (in seconds) for sending emails (e.g., 3600 = 1 hour)

    print("Starting IP monitor...")
    while True:
        current_ip = get_public_ip()
        if current_ip:
            if current_ip != last_sent_ip:
                print(f"New IP detected: {current_ip}")
                send_email(current_ip)
                last_sent_ip = current_ip
            else:
                print("IP address unchanged. No email sent.")
        else:
            print("Failed to retrieve public IP. Retrying later.")

        time.sleep(email_interval)
