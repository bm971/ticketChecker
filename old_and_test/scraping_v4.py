from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
import ssl
from email.message import EmailMessage

url = "https://tickets.funcode.hu/event/rammstein-allohely-2023"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
email_sender = "bm9711111111@gmail.com"
email_password = "mekueihigncngwqt"
email_receiver = "bakonyimark9785@gmail.com"

##########  A VERZIO
# message = """\
# Subject: VAN RAMMSTEIN JEEEEEGY!!!!!!!!!!!!!!!!!!!!!

# Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

# Itt a link te paraszt: https://tickets.funcode.hu/event/rammstein-allohely-2023

# ###############################################################################
# Reszletek:

# """
# mycontext = ssl.create_default_context()
# with smtplib.SMTP(smtp_server, port) as server:
#     server.ehlo()  # Can be omitted
#     server.starttls(context=mycontext)
#     server.ehlo()  # Can be omitted
#     server.login(email_sender, email_password)
#     server.sendmail(email_sender, email_receiver, message)

#################### B VERZIO
# def happyemail(body):
#     mycontext = ssl.create_default_context()
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.ehlo()  # Can be omitted
#         server.starttls(context=mycontext)
#         server.ehlo()  # Can be omitted
#         server.login(email_sender, email_password)
#         server.sendmail(email_sender, email_receiver, body)

### ORIGINAL STATUS when there is no aviailable ticket
# list of all "em" tags:
# [<em style="color: red;">Figyelem</em>, <em>Elfogyott</em>, <em>Elfogyott</em>, <em>Elfogyott</em>]
# original lenght of the availability array: 4
# the class I am interested in: <div class="purchase_tickets js-single-event" id="select-tickets" style="margin-top: 0px;">

def eredmeny(vanjegy):
    print(vanjegy)
    if vanjegy == True:
        for data in doc.findAll("div", {"id": "select-tickets"}): # print out the relevant section (the "select-tickets" class) of the website
            print(data)
            # message = """\
            # Subject: VAN RAMMSTEIN JEEEEEGY!!!!!!!!!!!!!!!!!!!!!

            # Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

            # Itt a link te paraszt: https://tickets.funcode.hu/event/rammstein-allohely-2023

            # ###############################################################################
            # Reszletek:

            # """
            # happyemail(message)
            message = """

            Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

            Itt a link te paraszt: https://tickets.funcode.hu/event/rammstein-allohely-2023

            ###############################################################################
            Reszletek:

            """
            mycontext = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=mycontext)
                server.ehlo()  # Can be omitted
                server.login(email_sender, email_password)
                server.sendmail(email_sender, email_receiver, message)

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