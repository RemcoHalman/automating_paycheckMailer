import logging
import os
import os.path as op
import smtplib
import sys
import threading
import time
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
from watchdog.observers import Observer

import email_config

PATH = email_config.PATH
MAIL_FROM = email_config.MAIL_FROM
EMAIL_STAFF_FIRSTNAME = email_config.EMAIL_STAFF_FIRSTNAME
EMAIL_STAFF_LASTNAME = email_config.EMAIL_STAFF_LASTNAME
EMAIL_STAFF_NAME = EMAIL_STAFF_FIRSTNAME + " " + EMAIL_STAFF_LASTNAME
EMAIL_TO_STAFF = email_config.EMAIL_TO_STAFF
EMAIL_SUBJECT = email_config.EMAIL_SUBJECT
CURRENT_TIME = time.asctime(time.localtime(time.time()))

logging.basicConfig(
    filename=f"~/logs/Payslip_Send_{EMAIL_STAFF_FIRSTNAME}.log",
    level=logging.INFO,
    format="%(asctime)s: (%(levelname)s) :%(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)


class SendMail:
    def send_email(self, EMAIL_TO, file_path):
        content = "".join(
            [
                f"""{email_config.TIME_GREETING} {EMAIL_STAFF_FIRSTNAME} {EMAIL_STAFF_LASTNAME},<br/>
                <br/>
                Bijgaande zit het loonstrookje van afgelopen maand<br/>
                Mochten hier verdere vragen over zijn hoor ik die graag.<br/>
                <br/>
                Met vriendelijke groet,<br/>
                <br/>
                Remco Halman <br/>
                Escaperoom Drachten<br/>
                <br/>
                <small><i>Deze mail is automatisch gegenereerd en verstuurt op: {CURRENT_TIME}</i></small>
                """
            ]
        )

        msg = MIMEMultipart()
        msg["Subject"] = EMAIL_SUBJECT
        msg["To"] = EMAIL_TO
        msg["From"] = MAIL_FROM

        msg.attach(MIMEText(content, "html"))

        # attachment file
        filename = os.path.basename(file_path)
        attachment = open(file_path, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= %s" % filename)
        msg.attach(part)

        mail = smtplib.SMTP(f"{email_config.SMTP_SERVER}")
        mail.connect(f"{email_config.SMTP_SERVER}", email_config.PORT)

        mail.starttls()
        mail.login(email_config.USERNAME, email_config.PASSWORD)
        mail.sendmail(MAIL_FROM, EMAIL_TO, msg.as_string())
        mail.quit()
        logging.info(f"Mail send to: {EMAIL_STAFF_NAME} with attachment: {filename}")


class Watchdog(PatternMatchingEventHandler, Observer):
    def __init__(self, path=PATH, patterns="*", logfunc=logging.info):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)
        self.schedule(self, path=path, recursive=True)
        self.log = logfunc

    def on_created(self, event):
        # This function is called when a file is created
        self.log(f"{event.src_path} has been created!")
        # obj = SendMail()
        # obj.send_email(EMAIL_TO_STAFF, event.src_path)

    def on_deleted(self, event):
        # This function is called when a file is deleted
        logging.warning(f"Someone deleted {event.src_path}!")


if __name__ == "__main__":
    observer = Watchdog()
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        print(e)
    observer.join()
