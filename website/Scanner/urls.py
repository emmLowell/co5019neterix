from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('scan', views.scan, name="scan"),
    path('contact', views.contact, name="contact"),
    path('report', views.report, name="report"),
]
