from flask_mail import Message
from app.core.notifications import NotificationHandler, Notifier
from app import mail
import sendgrid
from sendgrid.helpers.mail import Mail
import os


# from flask import render_template


class EmailNotification(NotificationHandler):
    email_parameters: dict
    # flask_mail
    """
    def send(self):
        msg = Message(**self.email_parameters)
        mail.send(msg)
    """

    # twilio sendgrid
    def send(self):
        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))
        msg = Mail(**self.email_parameters)
        sg.send(msg)
