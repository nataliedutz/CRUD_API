from django.urls import path
from . import views

app_name="tasks"

urlpatterns=[
    path("apitasks/", views.TaskListApi.as_view()),
    path("apitasks/<int:task_id>", views.TaskDetailApi.as_view()),
]
