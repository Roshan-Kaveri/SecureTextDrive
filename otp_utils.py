# otp_utils.py
import random
from flask_mail import Message



otp_storage = {}

def generate_otp(length=6):
    """Generate a random OTP of specified length."""
    otp = ''.join(random.choices("0123456789", k=length))
    return otp

def send_otp_email(mail, email, otp):
    """Send the OTP to the user's email."""
    try:
        msg = Message('Your OTP Code', sender='support@hmmbo.com', recipients=[email])
        msg.body = f"Your OTP code is: {otp}. Please use this code to proceed. It will expire in 10 minutes."
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
