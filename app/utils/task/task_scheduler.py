import os
from celery import shared_task
from sendgrid import sendgrid, Mail, SendGridAPIClient
from app.core.exceptions import AppException

EMAIL_PROVIDER_API = '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'


@shared_task
def send_email(email_parameters):
    try:
        sg = sendgrid.SendGridAPIClient(
            api_key=EMAIL_PROVIDER_API)
        msg = Mail(**email_parameters)
        sg.send(msg)
    except Exception as e:
        raise AppException.OperationError(context=e.args[0])
