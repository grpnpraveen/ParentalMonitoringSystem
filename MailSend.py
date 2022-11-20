from email.message import EmailMessage
import ssl 
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()


def Send(body="body",subject="subject",email_receiver=None):
    if email_receiver!=None:
        try:
            em=EmailMessage()
            em['From']=os.getenv("EMAIL_SENDER")
            em['To']=email_receiver
            em['subject']=subject
            em.set_content(body)
            context=ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(os.getenv("EMAIL_SENDER"),os.getenv("EMAIL_PASSWORD"))
                smtp.sendmail(os.getenv("EMAIL_SENDER"),email_receiver,em.as_string())
            return True,"Sent Successfully"
        except:
            return False,"Error in try block"
    else:
        return True,"invalid receiver mail"


