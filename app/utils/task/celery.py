from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# def make_celery(app=None):
#     app = app or create_app()
#     celery = Celery('app', backend=app.config['result_backend'], broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery

# def create_celery_app(app=None):
#     app = app or create_app(Config)
#     celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery

# def init_celery(app):
#     celery = Celery()
#     celery.conf.broker_url = app.config['CELERY_BROKER_URL']
#     celery.conf.result_backend = app.config['result_backend']
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         """Make celery tasks work with Flask app context"""
#
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
