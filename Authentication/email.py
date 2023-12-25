from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.response import Response
from decouple import config

import smtplib
from .elastic_email import ElasticEmailHelper


# def send_welcome_email(name,receiver,code):


#     # Render the email template with the context data
    
#     subject = "Email Verification"
#     new_message = f"""
#       CONGRATS {name}, YOU'RE IN!

#       Welcome to Nicedirect. We are thrilled to have you. 
#       Your email address has been verified but your account verification is in progress. 
#       Please bear with us as this may take a short while. Verify your email address using the code sent below.
#       Your Code is {code} 
#     """
#     plain_message = f"Subject: Email Verification \n\n{new_message}"
    

#     # Set the email subject, sender, recipient(s), and message content
#     from_email = config('EMAIL_HOST_USER')
#     recipient_list = [receiver]
#     # email_msg = EmailMessage(subject, new_message, from_email, recipient_list)
#     # email_msg.send()

#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['To'] = receiver
#     msg['Subject'] = subject

#     msg.attach(MIMEText(new_message, 'plain'))

#     server = smtplib.SMTP(config('EMAIL_HOST'),587)
#     server.starttls()
#     server.login(config('EMAIL_HOST_USER'),config('EMAIL_HOST_PASsWORD'))
#     server.sendmail(from_email, receiver, msg.as_string())
#     server.quit()

def send_welcome_email(name,receiver,code):
    helper = ElasticEmailHelper()
    to_email = receiver
    subject = "Email Verification"
    body = f"""
      CONGRATS {name}, YOU'RE IN!

      Welcome to Nicedirect. We are thrilled to have you. 
      Your email address has been verified but your account verification is in progress. 
      Please bear with us as this may take a short while. Verify your email address using the code sent below.
      Your Code is {code} 
    """
    response = helper.send_email(to_email, subject, body)

    # Handle the response (check for success or handle errors)
    if response['success']:
        return Response('Email sent successfully!')
    else:
        return Response('Failed to send email. Error: {}'.format(response['error']))
