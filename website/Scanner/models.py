from django.db import models


class Cve(models.Model):
    cve_id = models.IntegerField()
    cve = models.IntegerField()

    def __str__(self):
        return str(self.cve_id)


class IpCve(models.Model):
    ip = models.OneToOneField('Ip', on_delete=models.CASCADE, primary_key=True)
    cve = models.OneToOneField('Cve', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'IP: {self.ip}, CVE: {self.cve}'


class Scan(models.Model):
    scan_id = models.IntegerField(primary_key=True)
    scan_type = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    os = models.CharField(max_length=10)
    ip = models.ForeignKey('Ip', on_delete=models.CASCADE)

    def __str__(self):
        return f'Scan ID: {self.scan_id}'


class Ip(models.Model):
    ip_id = models.IntegerField(primary_key=True)
    ip_address = models.GenericIPAddressField(max_length=15)
    alias = models.CharField(max_length=15)

    def __str__(self):
        return self.ip_address


class IpPort(models.Model):
    scan = models.OneToOneField('Scan', on_delete=models.CASCADE, primary_key=True)
    ip = models.OneToOneField('Ip', on_delete=models.CASCADE, unique=True)
    port = models.OneToOneField('Port', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'IP: {self.ip}, Port: {self.port}'


class Port(models.Model):
    port_id = models.IntegerField(primary_key=True)
    port_number = models.IntegerField()
    service = models.CharField(max_length=30)

    def __str__(self):
        return str(self.port_number)


class Schedule(models.Model):
    ip = models.ForeignKey('Ip', on_delete=models.CASCADE)
    cron_time = models.CharField(max_length=50)
    scan_type = models.CharField(max_length=30)

    def __str__(self):
        return "Schedule<ip: {}, cron_time: {}, scan_type: {}>".format(self.ip, self.cron_time, self.scan_type)
