from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('scan', views.scan, name="scan"),
    path('contact', views.contact, name="contact"),
    path('reports', views.report, name="reports"),
    path('reports/<int:ip_id>', views.report_ip, name="report_ip"),
    path('reports/<int:ip_id>/<int:scan_id>', views.report_scan, name="report_scan"),
    
]