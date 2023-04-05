from django.conf import settings
from twilio.rest import Client
from django.core.cache import cache
import random


class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number=phone_number
        self.otp=otp
    def send_otp_via_message(self): 
        self.phone_number = 9645680693    
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{self.phone_number}')
    def send_otp_via_whatsapp(self):     
        self.phone_number = 9645680693
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(body=f'your otp is:{self.otp}',from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_number}')

    def generate_otp(self,user_id):
    # Generate a random 6-digit OTP
        otp = random.randint(1000, 9999)
    
    # Store the OTP in the cache for 5 minutes
        cache.set(f'otp_{user_id}', otp, 600)
    
        return otp


    def validate_otp(user_id, otp):
    # Retrieve the OTP from the cache
        cached_otp = cache.get(f'otp_{user_id}')
    
    # Check if the OTP matches the cached value
        if str(cached_otp) == str(otp):
        # OTP is valid
            cache.delete(f'otp_{user_id}') # Remove otp from cache
            return True
        else:
        # OTP is invalid
            return False