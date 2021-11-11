from app import init_celery


app = init_celery()
print("app in celery app", app)
app.conf.imports = app.conf.imports + ("app.utils.tasks",)
