from app.core.notifications import NotificationHandler
from app.core.exceptions import AppException


class EmailNotification(NotificationHandler):
    email_parameters: dict

    def send(self):
        from app.utils.tasks import send_mail
        try:
            send_mail.delay(self.email_parameters)
        except send_mail.OperationalError as exc:
            raise AppException.OperationError(context=exc.args[0])
