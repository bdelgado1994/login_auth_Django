from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("singup", views.create_user, name="singup"),
    path("task", views.task_page, name="task"),
    path("logout", views.close_session, name="logout"),
    path("login", views.singin, name="login"),
    path("task/create", views.create_task, name="create_task"),
    path("task/<int:id_task>", views.task_detail, name="task_detail"),
    path("task/delete/<int:id_task>",views.delete_task,name="delete_task"),
    path("task/completed",views.tasks_completed,name="tasks_completed")
]
