# importing reqiored modules
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# user credentials 
SENDER_EMAIL = "dantavaidya@gmail.com" # your email address
PASSKEY = "fpng oeai qyqo jlcd" # app passkey
# smtp server
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# email send function defination
def emailSend(to_email:str, header:str, body:str):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = header
        msg.attach(MIMEText(body, 'plain')) # attach body 

        # server connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() #start server securly
        server.login(SENDER_EMAIL, PASSKEY) # login to server
        server.sendmail(from_addr=SENDER_EMAIL, 
                        to_addrs=to_email, 
                        msg = msg.as_string()) # send mail
        server.quit()
    except Exception as e:
        return f"Something wrong in email send:{e}"
