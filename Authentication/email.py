from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.response import Response
from decouple import config

import smtplib
from .elastic_email import ElasticEmailHelper


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
    

def send_forgotten_passowrd_email(receiver):
    link = 'https://nike.com'
    helper = ElasticEmailHelper()
    to_email = receiver
    subject = "Password Recovery"
    body = f"""
      Hi,

 

To reset your Nicedirectcoffee account password please\n\n go to: {link}.

If you have previously requested to change your password, only the link contained in this e-mail is valid.

 

If this wasn't you:

Your Nicedirectcoffee account may have been compromised and you should take a few steps to make sure it is secure. To start, reset your password now. If you have not yet added 2 Steps-Verification protection to your account, we highly recommend you to activate the feature now to enhance the security of your account and prevent unauthorized access.

 

Sincerely,

Your Nicedirectcoffee team 
    """
    response = helper.send_email(to_email, subject, body)

    # Handle the response (check for success or handle errors)
    if response['success']:
        print('success')
        return Response('Email sent successfully!')
    else:
        return Response('Failed to send email. Error: {}'.format(response['error']))
