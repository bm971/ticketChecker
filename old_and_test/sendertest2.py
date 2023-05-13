from email.message import EmailMessage
import smtplib
import ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
email_sender = "bm9711111111@gmail.com"
email_password = "mekueihigncngwqt"
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
        server.ehlo()  # Can be omitted
        server.starttls(context=mycontext)
        server.ehlo()  # Can be omitted
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, em.as_string())

mybody = """
Van jegy, kurva gyorsan vegyel!!!!!!!!!!!!

Itt a link te paraszt: https://tickets.funcode.hu/event/rammstein-allohely-2023

###############################################################################
Reszletek:

"""

happymail(mybody)