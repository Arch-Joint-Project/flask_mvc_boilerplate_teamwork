from app.core.notifications import NotificationHandler
from app.core.exceptions import AppException



class EmailNotification(NotificationHandler):
    email_parameters: dict
    # sg: sendgrid
    # msg: Mail

    # def __init__(self):
    #     self.sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    #     # self.msg = Mail(**self.email_parameters)

    def send(self):
        from app.utils.task import task_send_email
        try:
            task_send_email.delay(self.email_parameters)
        except Exception as e:
            raise AppException.OperationError(context=e.args[0])
