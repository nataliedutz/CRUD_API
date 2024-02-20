from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_name=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now=True)
    completed=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
