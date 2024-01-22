#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

from email.message import EmailMessage
import smtplib
import ssl
import datetime
import logging
import re

import pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()

datetag = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
#filemsg = []
logging.basicConfig(level=logging.INFO, filename='/var/log/scripts/ticketChecker/scraping_result.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

url = "https://tickets.efinity.rs/CardType/EventInfo?cardTypeId=30621" # event date: 25.05.2024 for TEST purpuses
#url = "https://tickets.efinity.rs/CardType/EventInfo?cardTypeId=30620" # event date: 24.05.2024 -> desired date
try:
    result = requests.get(url)
    print('SIKERES scraping')
except Exception as sucks:
    filemsg = "Gebasz: \n"+sucks
    logging.info(filemsg)
    print('uzenet ha nem sikerult ha SIKERTELEN!!! scraping, hibauzenet: '+filemsg)
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
                filemsg = """Volt elado jegy """+datetag+"""-kor:DDDDDDD
                """+str(data)
                print('filemsg, ez keril a logba: uzenet+teljes HTML class: '+filemsg)
            except Exception as sucks:
                filemsg = "Gebasz: \n"+sucks
                logging.info(filemsg)
                print(filemsg)
    else:
        filemsg = """Nem volt elado jegy """+datetag+"""-kor:(((((
        """+str(data)
        print('filemsg, ez keril a logba: uzenet+teljes HTML class: '+filemsg)
    logging.info(filemsg)

def compare_strings(string2compare,mypattern):
    pattern = re.compile(mypattern)
    match = re.search(pattern, string2compare)
    if match:
        print(f" comparing: '{mypattern}' found in '{string2compare}' TRUE")
        return True
    else:
        print(f" comparing:'{mypattern}' not found in '{string2compare}' FALSE")
        return False

############# Start of action ################

patterntext1 = 'FeuerZone'
patterntext2 = 'SOLD'
interestingSection = doc.findAll("p")
print('interestingSection, itt van az osszes p sor amit keresek: '+str(interestingSection))
lengthOfInterest = len(interestingSection) # number of elements in the interestingSection array
print('lengthOfInterest, osszes p amit talalt a vizsgalt reszben, interestingSection array szamossaga: '+str(lengthOfInterest))

for i in range(1,lengthOfInterest): # miert 1-tol kezdodik???
    try:
        string2check = interestingSection[i].string
        print('string to check, actual element of array: '+string2check)
        if compare_strings(string2check, patterntext1) == True:
            if compare_strings(string2check, patterntext2) == True:
                createAndSendMail(True)
            else:
                createAndSendMail(False)
    except:
        createAndSendMail(True) # lehet eleg lenne break is de biztosra megyek inkabb