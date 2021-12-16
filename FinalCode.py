import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
from datetime import datetime
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
gmail_user = "your gmail" 
gmail_pwd = "your gmail's pass" 
to = "your gmail" 
subject = ("Guvenlik Ihmali") #It's Turkish but you can use "Security Alert!" etc.
text = ("Hareketlilik var!")  #It's Turkish but you can use "There's a motion!" etc.

sensor = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

while True:
    previous_state = current_state
    current_state = GPIO.input(sensor)

    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor, new_state))
	if current_state:
		cap = cv2.VideoCapture(0)
	        ret, frame = cap.read()
		cap = cv2.VideoCapture(0)
		print "Fotograf Kaydediliyor..." #It's Turkish but you can use "Photo saving..." etc.
		picname = datetime.now().strftime("%y-%m-%d-%H-%M")
		picname = picname+'.jpg'
                cv2.imwrite(picname, frame)
		print "E-mail Gonderiliyor..." #It's Turkish but you can use "E-mail sending..." etc.
		
		attach = picname
		
		msg = MIMEMultipart()

		msg['From'] = gmail_user
		msg['To'] = to
		msg['Subject'] = subject

		msg.attach(MIMEText(text))

		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(attach, 'rb').read())
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition',
   		'attachment; filename="%s"' % os.path.basename(attach))
		msg.attach(part)

		mailServer = smtplib.SMTP("smtp.gmail.com", 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to, msg.as_string())
		# Should be mailServer.quit(), but that crashes...
		mailServer.close()
		print "E-mail Gonderildi" #It's Turkish but you can use "E-mail sent!" etc.
		os.remove(picname)
