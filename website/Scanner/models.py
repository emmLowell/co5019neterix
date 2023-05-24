from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from collections import defaultdict

class Cve(models.Model):
    cve_id = models.AutoField(primary_key=True)
    scan = models.ForeignKey("Scan", on_delete=models.CASCADE)
    port = models.ForeignKey("Port", on_delete=models.CASCADE)
    cve = models.CharField(max_length=50)

    def __str__(self):
        return "<CVE: {}>".format(self.cve)

class Scan(models.Model):
    ip = models.ForeignKey("Ip", on_delete=models.CASCADE)
    scan_id = models.AutoField(primary_key=True)
    scan_type = models.CharField(max_length=30)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    os = models.CharField(max_length=10)
    error = models.BooleanField(default=False)
    nmap_params = models.TextField(blank=True)
    
    @staticmethod
    def get_latest_scan(ip: 'Ip') -> Optional['Scan']:
        try:
            return Scan.objects.filter(ip=ip).latest('end_time')
        except Scan.DoesNotExist:
            return None
        
    def ports(self):
        return Port.objects.filter(scan=self)
    
    def cves(self):
        return Cve.objects.filter(scan=self)
        
    def ports_to_cve(self):
        cve_dict = defaultdict(list)
        ports = self.ports()
        for port in ports:
            cves = Cve.objects.filter(scan=self, port=port)
            for cve in cves:
                cve_dict[port.port_number].append(cve.cve)
        return dict(cve_dict)
    
    def status(self):
        if(self.error):
            return "Failed"
        if self.end_time is None:
            return "Scanning"
        return "Completed"
    
    def link(self):
        return f'/reports/{self.ip_id}/{self.scan_id}'
    

    def __str__(self):
        return f"<Scan: {self.ip}, {self.scan_type}, {self.start_time}, {self.end_time}, {self.os}, {self.error}, {self.nmap_params}>"

class Port(models.Model):
    port_id = models.AutoField(primary_key=True)
    scan = models.ForeignKey("Scan", on_delete=models.CASCADE)
    port_number = models.IntegerField()
    service = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"<Port: {self.port_number}, {self.service}>"

class Ip(models.Model):
    ip_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(max_length=15)
    alias = models.CharField(max_length=15)
    
    def link(self):
        return f'/reports/{self.ip_id}'

    def schedule_link(self):
        return f'/schedule/{self.ip_id}'

    def __str__(self):
        return f"<Ip: ip:{self.ip_address} alias:{self.alias}>"


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey("Ip", on_delete=models.CASCADE)
    cron_time = models.CharField(max_length=50)
    scan_type = models.CharField(max_length=30)
    port_type = models.CharField(max_length=30)
    
    def __str__(self):
        return "Schedule<ip: {}, cron_time: {}, scan_type: {}, port_type: {}>".format(
            self.ip, self.cron_time, self.scan_type, self.port_type
        )
        
    def delete_link(self):
        return f'/schedule/remove/{self.id}'