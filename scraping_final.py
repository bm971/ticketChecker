#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

from email.message import EmailMessage
import smtplib
import ssl
import datetime
import logging

import pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()

datetag = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
filemsg = []
logging.basicConfig(level=logging.INFO, filename='/var/log/scripts/ticketChecker/scraping_result.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

url = "https://tickets.efinity.rs/CardType/EventInfo?cardTypeId=30621" # 25.05.2024
#url = "https://tickets.efinity.rs/CardType/EventInfo?cardTypeId=30620" # 24.05.2024
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
with open(scriptpath/'.AUTH', 'r') as f:
    email_password = f.readline().strip()
    email_sender = f.readline().strip()
    email_receiver = f.readline().strip()
subject = "VAN RAMMSTEIN JEEEEEGY!!!!!!!!!!!!!!!!!!!!!"

def happymail(body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    mycontext = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=mycontext)
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, em.as_string())

### ORIGINAL STATUS when there is no aviailable ticket
# <p>TICKET PRICES:&#xD;&#xA;</p>
# <p>GA/Standing: 8.900 RSD</p>
# <p>FeuerZone: SOLD OUT</p>
# <p>Seating: SOLD OUT</p>
# <p>Important Notice:&#xD;&#xA;</p>

def createAndSendMail(ticketAvailable):
    if ticketAvailable == True:
        while True:
            try:
                for data in doc.findAll("div", {"class": "text-container"}): # print out the relevant section (the "text-container" class) of the website
                    print(data)
                happymessage = """
                Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

                Itt a link:"""+url+"""

                ###############################################################################
                Reszletek:

                """
                happymessage += str(data)
                happymail(happymessage)
                filemsg.append("Volt elado jegy"+datetag+"-kor:DDDDDDD")
            except Exception as szopo:
                logging.info("Gebasz: \n"+szopo)
    else:
        filemsg.append("Nem volt elado jegy "+datetag+"-kor:(((((")
    logging.info(filemsg)
    # logfile = open("/var/log/scripts/ticketChecker/"+filename, "w")
    # logfile.write(str(filemsg))
    # logfile.close()

availability = doc.findAll("p")
ticketTypeNumber = len(availability) # number of elements in the availability array

for i in range(1,ticketTypeNumber):
    try:    
        if availability[i].string != 'FeuerZone: SOLD OUT':
            createAndSendMail(True)
        else:
            createAndSendMail(False)
    except:
        createAndSendMail(True) # lehet eleg lenne break is de biztosra megyek inkabb