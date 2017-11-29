#!/usr/bin/env python
from env import getEnv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime

threshold_l = 67.5
threshold_h = 76.5
recips = ['john.stange@eglobaltech.com', 'ryan.bolyard@eglobaltech.com']
sender = "hvac-shaming@egt-labs.com"

resp = getEnv()
if(resp["temperature"] < threshold_l or resp["temperature"] > threshold_h):
  now = datetime.datetime.now()
  body = str(resp["temperature"])+" degrees Fahrenheit as of "+now.strftime("%Y-%m-%d %H:%M")
  print(body)
  msg = MIMEMultipart()
  msg['Subject'] = "Temperature readout in 742"
  msg['From'] = sender
  msg['To'] = ",".join(recips)
  msg.attach(MIMEText(body, 'plain'))
#s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
#s.starttls()
#s.login(MY_ADDRESS, PASSWORD)
  s = smtplib.SMTP("localhost")
  s.sendmail(msg['From'], recips, msg.as_string())
