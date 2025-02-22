import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#Invia una copia cifrata del database via email.
#SMTP Gmail permette backup automatizzati.
#Allegato cifrato protegge i dati.

EMAIL_SENDER = "ciberuam66@gmail.com"
EMAIL_PASSWORD = "ciberseguri"
EMAIL_RECEIVER = "ciberuam66@gmail.com"

def send_backup():
    """Invia il database cifrato via email."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Backup SecureBox"

    filename = "securebox.db"
    attachment = open(filename, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()

    print("Backup inviato con successo via Gmail!")
