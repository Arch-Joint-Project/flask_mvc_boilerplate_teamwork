# EMAIL_PROVIDER_API = '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'


from flask_mail import Message
from app import mail
from app.celery_app import app

print("this is the app", app)


@app.task
def send_mail(email_info: dict):
    msg = Message(
        subject=email_info.get("subject"),
        sender=email_info.get("from_email"),
        recipients=[email_info.get("to_emails")],
        body=email_info.get("body"),
        html=email_info.get("html_content")
    )
    mail.send(msg)

# @celery.task
# def send_email(email_parameters):
#     try:
#         sg = sendgrid.SendGridAPIClient(
#             api_key=EMAIL_PROVIDER_API)
#         msg = Mail(**email_parameters)
#         sg.send(msg)
#     except Exception as e:
#         raise AppException.OperationError(context=e.args[0])
