import abc
# from dataclasses import dataclass


class NotificationHandler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "send")) and callable(subclass.send)

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError
#
# @dataclass
# class MyNotificationHandler(abc.ABC):
#     @abc.abstractmethod
#     def send(self):
#         raise NotImplementedError
