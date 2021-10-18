from app.core.notifications import NotificationHandler
from app.core.exceptions import AppException


class EmailNotification(NotificationHandler):
    email_parameters: dict

    def send(self):
        from app.utils.task import send_email
        try:
            send_email.delay(self.email_parameters)
        except send_email.OperationalError as exc:
            raise AppException.OperationError(context=exc.args[0])
