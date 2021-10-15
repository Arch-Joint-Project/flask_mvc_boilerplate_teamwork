from app.core.notifications import NotificationHandler


class EmailNotification(NotificationHandler):
    email_parameters: dict

    def send(self):
        from app.utils.task import task_send_email
        task_send_email.delay(self.email_parameters)
