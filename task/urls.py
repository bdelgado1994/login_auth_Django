from django.urls import path
from . import views
urlpatterns=[
    path("",views.home,name="home"),
    path("singup",views.create_user,name="singup"),
    path("task",views.task_page,name="task"),
    path("logout",views.close_session,name="logout"),
    path("login",views.singin,name="login")
]