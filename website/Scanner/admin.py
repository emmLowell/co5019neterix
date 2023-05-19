from django.contrib import admin
from .models import Cve, Ip_cve, Ip_port, Scan, Ip, Port


admin.site.register([Cve, Ip_cve, Ip_port, Scan, Ip, Port])
