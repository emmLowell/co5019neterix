from django.contrib import admin
from .models import Cve, Scan, Ip, Port, IpCve, IpPort


admin.site.register([Cve, Scan, Ip, Port, IpCve, IpPort])


admin.site.site_header = 'Vulnerability Scanner'
admin.site.site_title = 'Neterix'
