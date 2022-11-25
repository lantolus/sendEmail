#!/usr/bin/python3
import os
import smtplib
import http.client
import json
import logging

sender='antollukas6@gmail.com'
password=os.environ.get("e_password")
receivers=os.environ.get("SKIT_ALERT_EMAIL")
smtpHost=os.environ.get("smtpHost")
smtpPort=os.environ.get("smtpPort")

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

conn = http.client.HTTPSConnection("status.digitalocean.com")
conn.request("GET", "/api/v2/status.json")
res=conn.getresponse()
logging.info(res.status, res.reason)
data=json.loads(res.read())
indicator=(data["status"]["indicator"])
conn.close()
if indicator=='major' or indicator=='critical':
    text=data
    subject="Subject"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    server = smtplib.SMTP(smtpHost, smtpPort )
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receivers, message)
    server.quit()
    logging.warning('Mail was sent to recipient!')


