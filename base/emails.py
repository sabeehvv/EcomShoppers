

import imp
from django.conf import settings
from django.core.mail import send_mail




def send_email_otp(email , otp):
    tempemail = email
    subject = 'Shoppers verification ONE TIME PASSWORD'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, Your ONE TIME PASSWORD to varify your account is {otp}'
    send_mail(subject , message , email_from , [tempemail])