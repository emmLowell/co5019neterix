from django.contrib import admin
from .models import Cve,Ip_cve,Ip_port,Scan,Ip,Port


admin.site.register(Cve)
admin.site.register(Ip_cve)
admin.site.register(Ip_port)
admin.site.register(Scan)
admin.site.register(Ip)
admin.site.register(Port)



