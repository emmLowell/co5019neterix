from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('scan', views.scan, name="scan"),
    path('contact', views.contact, name="contact"),
    path('signup', views.signup, name="signup"),
    path('recover', views.recover, name="recover"),
    path('recover2', views.recover2, name="recover2"),
    path('recover3', views.recover3, name="recover3"),
    path('reports', views.report, name="reports"),
    path('home', views.home, name="home"),
]
