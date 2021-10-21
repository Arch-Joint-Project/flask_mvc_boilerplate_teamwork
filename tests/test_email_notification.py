from tests import BaseTestCase
import pytest
import unittest
from app.core.notifications.notifier import Notifier
from app.services.email_service import EmailNotification

email_notification = EmailNotification()
notifier = Notifier()

email_parameters = {
    "from_email": "michaelasumadu1@outlook.com",
    "to_emails": "michaelasumadu1@gmail.com",
    "subject": f"Invoice",
    "html_content": "<b> name</b>"
}
# patch_send = patch("app.utils.task.task_scheduler.send_email.sg.send")
# patch_send.return_value = "patch"
# print("this is th ", patch_send.return_value)


class TestEmailNotification(BaseTestCase):
    # @pytest.mark.active
    # def test_notifier_notify(self):
    #     with patch("app.services.email_service.EmailNotification.send") as mock:
    #         # email_notification.email_parameters = email_parameters
    #         notifier.notify(email_notification)
    #     self.assertTrue(mock.called)
    #     # self.assertTrue(mock.call_args(email_parameters))

    # @pytest.mark.active
    # def test_email_notification_send(self):
    #     with patch("app.utils.task.task_scheduler.send_email") as mock:
    #         email_notification.email_parameters = email_parameters
    #         email_notification.send()
    #     self.assertTrue(mock.assert_called)
    #     # self.assertEqual(mock.return_value, "patch")

    @pytest.mark.active
    def test_delay(self):
        email_notification.email_parameters = email_parameters
        email_notification.send()

        # with patch("app.utils.task.task_scheduler.make_celery", make_celery(self.redis)) as mock_celery:
        #     print(mock_celery)
        #     with patch("app.utils.task.task_scheduler.send_email") as mock:
        #         print(mock)
        #         email_notification.email_parameters = email_parameters
        #         email_notification.send()

        # with patch("app.utils.task.celery.make_celery") as mock_celery:
        #     with patch("app.utils.task.task_scheduler.celery") as c:
        #         c = mock_celery(self.redis)
        #         with patch("app.utils.task.task_scheduler.send_email") as mock:
        #             email_notification.email_parameters = email_parameters
        #             email_notification.send()
        #     self.assertTrue(mock.assert_called)
        #     #     # self.assertEqual(mock.return_value, "patch")
            # print(app.utils.task.task_scheduler.make_celery)
            # print(mock_celery)
            # mock_celery(self.redis)
            # print(mock_celery.call_args)
            # print(mock_celery(self.redis))



if __name__ == "__main__":
    unittest.main()
