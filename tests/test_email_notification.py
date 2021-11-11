from tests import BaseTestCase
import pytest
import unittest
from app.core.notifications.notifier import Notifier
from app.services.email_service import EmailNotification
from unittest.mock import patch
from app import init_celery
# from app.celery_app import init_celery


email_notification = EmailNotification()
notifier = Notifier()

email_parameters = {
    "from_email": "michaelasumadu1@outlook.com",
    "to_emails": "michaelasumadu1@gmail.com",
    "subject": f"Invoice",
    "html_content": "<b> name</b>"
}


class TestEmailNotification(BaseTestCase):
    @pytest.mark.email
    def test_notifier_notify(self):
        with patch("app.services.email_service.EmailNotification.send") as mock_send:
            notifier.notify(email_notification)
        self.assertTrue(mock_send.called)
        self.assertEqual(mock_send.call_count, 1)

    @pytest.mark.email
    def test_email_notification_send(self):
        with patch("app.init_celery",  side_effect=self.init_celery) as mock_celery:
        # with patch.object(app, "init_celery", return_value=init_celery(self.create_app())) as mock_celery:
            with patch("app.utils.tasks.send_mail.delay") as mock_celery_delay:
                print(mock_celery)
                email_notification.email_parameters = email_parameters
                email_notification.send()
        # self.assertTrue(mock_celery.called)
        self.assertTrue(mock_celery_delay.called)
        self.assertEqual(mock_celery_delay.call_count, 1)


    # @pytest.mark.email
    # def test_email_notification_send(self):
    #     # with patch("app.utils.task.init_celery")
    #     with patch("app.utils.tasks.send_mail.delay") as mock_celery_delay:
    #         email_notification.email_parameters = email_parameters
    #         email_notification.send()
    #     self.assertTrue(mock_celery_delay.called)
    #     self.assertEqual(mock_celery_delay.call_count, 1)


if __name__ == "__main__":
    unittest.main()
