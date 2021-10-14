from app.core.notifications import NotificationHandler
import sendgrid
from sendgrid.helpers.mail import Mail
import os
from app.core.exceptions import AppException, HTTPException


class EmailNotification(NotificationHandler):
    email_parameters: dict

    def send(self):
        try:
            sg = sendgrid.SendGridAPIClient(
                api_key=os.environ.get('SENDGRID_API_KEY'))
            msg = Mail(**self.email_parameters)
            sg.send(msg)
        except Exception as e:
            raise AppException.BadRequest(context=e.args[0])
