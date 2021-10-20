import os

from celery import shared_task
from sendgrid import sendgrid, Mail
#from .prep_celery import make_celery
from app.core.exceptions import AppException



@shared_task
def send_email(email_parameters):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))
        msg = Mail(**email_parameters)
        sg.send(msg)
    except Exception as e:
        raise AppException.BadRequest(context=e.args[0])
