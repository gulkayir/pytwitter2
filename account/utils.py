
from celery import shared_task
from django.core.mail import send_mail
from twitter_api._celery import app

from django.core.mail import send_mail


@app.task
def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""
    Thank you for registrate in our PyTwitter app!
    To activate your account click here {activation_url}
    """

    send_mail('PyTwitter account activation',message,'admin@admin.com', [email, ], fail_silently=False, )

@app.task
def send_activation_mail(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""
    Use this code to reset {activation_code}
"""

    send_mail('Pytwitter password reset',message,'admin@admin.com', [email, ], fail_silently=False, )
