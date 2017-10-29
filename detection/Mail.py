#!/usr/bin/env python3
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

def send_mail( send_from, send_to, subject, text, filesdir,max_pictures ,server="localhost", port=587, username='', password='', isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )
    picture_counter=0
    for f in os.listdir(filesdir):
        if f.endswith(".jpg"):
            if picture_counter<max_pictures:
                #print("Add attachment: "+os.path.join(filesdir, f))
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(filesdir+f,"rb").read() )
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
                msg.attach(part)
                picture_counter=picture_counter+1

    try:
        smtp = smtplib.SMTP(server, port)
        if isTls: smtp.starttls()
        smtp.login(username,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
    except:
        return False
    return True
