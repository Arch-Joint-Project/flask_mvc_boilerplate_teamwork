import os
from sendgrid import sendgrid, Mail
from .celery import make_celery
from app import create_app
from app.core.exceptions import AppException

celery = make_celery(create_app())


@celery.task
def task_send_email(email_parameters):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))
        msg = Mail(**email_parameters)
        sg.send(msg)
    except Exception as e:
        raise AppException.BadRequest(context=e.args[0])
