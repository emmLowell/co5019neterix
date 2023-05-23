from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('scan/', views.scan, name="scan"),
    path('contact/', views.contact, name="contact"),
    path("add-ip/", views.add_ip, name="add_ip"),
    path('reports/', views.report, name="reports"),
    path('reports/<int:ip_id>', views.report_ip, name="report_ip"),
    path('reports/<int:ip_id>/<int:scan_id>', views.report_scan, name="report_scan"),
    path("schedule/", views.schedule, name="schedule"),
    path("schedule/<int:schedule_id>/delete", views.delete_schedule, name="delete_schedule" ),
    path("schedule/<int:schedule_id>", views.schedules, name="schedule_id"),
]