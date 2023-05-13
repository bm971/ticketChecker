from bs4 import BeautifulSoup
import requests
import datetime

from email.message import EmailMessage
import smtplib
import ssl

url = "https://tickets.funcode.hu/event/rammstein-allohely-2023"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

emailbody = """Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

Itt a link te paraszt: https://tickets.funcode.hu/event/rammstein-allohely-2023

###############################################################################
Reszletek:

"""

email_sender = 'bm9711111111@gmail.com'
email_password = 'mekueihigncngwqt'
email_receiver = 'bakonyimark9785@gmail.com'
subject = 'VAN RAMMSTEIN JEEEEEGY!!!!!!!!!!!!!!!!!!!!!'

def happyemail(body):
    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.set_content(body)

    emailcontext = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=emailcontext) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string)

### ORIGINAL STATUS when there is no aviailable ticket
# list of all "em" tags:
# [<em style="color: red;">Figyelem</em>, <em>Elfogyott</em>, <em>Elfogyott</em>, <em>Elfogyott</em>]
# original lenght of the availability array: 4
# the class I am interested in: <div class="purchase_tickets js-single-event" id="select-tickets" style="margin-top: 0px;">

def eredmeny(vanjegy):
    print(vanjegy)
    if vanjegy == True:
        emailbody2 = ""
        # emailbody.append("Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!\nItt a link te paraszt: "+url+"\n#####################################\nReszletek: \n\n")
        for data in doc.findAll("div", {"id": "select-tickets"}): # print out the relevant section (the "select-tickets" class) of the website
            emailbody2 += str(data)
        emailbody += emailbody2
        print(emailbody)
        # happyemail(emailbody)

availability = doc.findAll("em")
ticketTypeNumber = len(availability) # number of elements in the availability array
if ticketTypeNumber != 4: # if the array lenght is different from the original (4)
    eredmeny(True)
print('Az "em" tagek száma: '+str(ticketTypeNumber))
print('Az osszes "em" tag tartalma: '+str(availability))

### TEST, torold majd ki!!!!
availability.pop(3)
#availability.append(<em>Elfogyott</em>)
#print(type(availability[1]))
print('Csokkentett em tages array: '+str(availability))

for i in range(1,ticketTypeNumber):
    try:    
        print(availability[i].string)
        if availability[i].string != 'Elfogyott':
            eredmeny(True)
        else:
            eredmeny(False)
    except:
        eredmeny(True) # lehet eleg lenne break is de biztosra megyek inkabb