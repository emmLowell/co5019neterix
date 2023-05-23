from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("recover2", views.recover2, name="recover2"),
    path("recover3", views.recover3, name="recover3"),
    path("recover", views.recover, name="recover"),
]