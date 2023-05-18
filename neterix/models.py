from django.db import models

class Cve(models.Model):
    cve_id=models.IntegerField(primary_key=True)
    cve = models.IntegerField()

class Ip_cve(models.Model):
    scan_id=models.IntegerField(primary_key=True)
    ip_id=models.IntegerField(unique=True)
    cve_id=models.IntegerField(unique=True)

class Scan(models.Model):
    scan_id=models.IntegerField(primary_key=True)
    scan_type=models.CharField(max_length=30)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    os=models.CharField(max_length=10)
    ip_id =models.IntegerField()

class Ip(models.Model):
    ip_id=models.IntegerField(primary_key=True)
    ip_address=models.GenericIPAddressField(max_length=15)
    alias=models.CharField(max_length=15)

class Ip_port(models.Model):
    scan_id = models.IntegerField(primary_key=True)
    ip_id=models.IntegerField(unique=True)
    port_id=models.IntegerField(unique=True)

class Port(models.Model):
    port_id=models.IntegerField(primary_key=True)
    port_number=models.IntegerField()
    service=models.CharField(max_length=30)