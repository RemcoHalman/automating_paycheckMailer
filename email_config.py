import os
import time

USERNAME = os.environ.get("WORK_MAIL_USER")
PASSWORD = os.environ.get("WORK_MAIL_PASS")
PORT = os.environ.get("WORK_MAIL_PORT")
SMTP_SERVER = os.environ.get("WORK_MAIL_SMTP")
MAIL_FROM = os.environ.get("MAIL_CONTACTNAME")
EMAIL_STAFF_FIRSTNAME = "<Staff Firstname>"
EMAIL_STAFF_LASTNAME = "<Staff Lastname>"
EMAIL_TO_STAFF = "<Email Staff>"
EMAIL_SUBJECT = "<Email Subject>"

PATH = "<Path to watch>"
TIME_GREETING = ""  # Auto filled in

now = time.localtime()
current_hour = now.tm_hour

if current_hour < 12:
    TIME_GREETING = "Goedemorgen"  # Good Morning
elif current_hour >= 12:
    TIME_GREETING = "Goedemiddag"  # Good Afternoon
else:
    TIME_GREETING = "Goedenavond"  # Good Evening
