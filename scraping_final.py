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

auth = open(scriptpath/".AUTH","r")
gmailpwd = auth.read()
auth.close()

datetag = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
filemsg = []
logging.basicConfig(level=logging.INFO, filename='/var/log/scripts/ticketChecker/scraping_result.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

url = "https://tickets.funcode.hu/event/rammstein-allohely-2023"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
email_sender = "bm9711111111@gmail.com"
email_password = gmailpwd
email_receiver = "bakonyimark9785@gmail.com"
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
# list of all "em" tags:
# [<em style="color: red;">Figyelem</em>, <em>Elfogyott</em>, <em>Elfogyott</em>, <em>Elfogyott</em>]
# original lenght of the availability array: 4
# the class I am interested in: <div class="purchase_tickets js-single-event" id="select-tickets" style="margin-top: 0px;">

def createAndSendMail(ticketAvailable):
    if ticketAvailable == True:
        while True:
            try:
                for data in doc.findAll("div", {"id": "select-tickets"}): # print out the relevant section (the "select-tickets" class) of the website
                    print(data)
                happymessage = """
                Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

                Itt a link te: https://tickets.funcode.hu/event/rammstein-allohely-2023

                ###############################################################################
                Reszletek:

                """
                happymessage += str(data)
                happymail(happymessage)
                filemsg.append("Volt elado jegy"+datetag+"-kor:DDDDDDD")
            except Exception as e:
                logging.info("Gebasz: \n"+e)
    else:
        filemsg.append("Nem volt elado jegy "+datetag+"-kor:(((((")
    logging.info(filemsg)
    # logfile = open("/var/log/scripts/ticketChecker/"+filename, "w")
    # logfile.write(str(filemsg))
    # logfile.close()

availability = doc.findAll("em")
ticketTypeNumber = len(availability) # number of elements in the availability array
if ticketTypeNumber != 4: # if the array lenght is different from the original (4)
    createAndSendMail(True)

for i in range(1,ticketTypeNumber):
    try:    
        if availability[i].string != 'Elfogyott':
            createAndSendMail(True)
        else:
            createAndSendMail(False)
    except:
        createAndSendMail(True) # lehet eleg lenne break is de biztosra megyek inkabb