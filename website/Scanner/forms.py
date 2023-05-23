from apscheduler.triggers.cron import CronTrigger

from .models import Schedule, Ip
from django import forms

class IpForm(forms.ModelForm):
    class Meta:
        model = Ip
        fields = ['ip_address', 'alias']


class ScanForm(forms.Form):
    SCAN_CHOICES = [
        ('stealth', 'Stealth'),
        ('normal', 'Normal'),
    ]

    PORT_CHOICES = [
        ('common', 'Common'),
        ('all', 'All'),
    ]

    scan_type = forms.ChoiceField(label='Scan Type', choices=SCAN_CHOICES)
    ports = forms.ChoiceField(label='Ports', choices=PORT_CHOICES)
    ips = forms.ChoiceField(label='IPs')

    def __init__(self, user, *args, **kwargs):
        super(ScanForm, self).__init__(*args, **kwargs)
        self.fields['ips'].choices = self.get_ip_choices(user)

    def get_ip_choices(self, user):
        # Retrieve the list of IPs based on the current user
        ips = Ip.objects.filter(user=user)
        choices = [(ip.ip_id, f"{ip.alias} - {ip.ip_address}") for ip in ips]
        return choices

    def has_ips(self):
        return len(self.fields['ips'].choices) > 0



class ScheduleForm(forms.Form):
        
    minute = forms.CharField(label='Minute', max_length=5, initial='0')
    hour = forms.CharField(label='Hour', max_length=5, initial='0')
    day_of_month = forms.CharField(label='Day of Month', max_length=5, initial='*')
    month = forms.CharField(label='Month', max_length=5, initial='*')
    day_of_week = forms.CharField(label='Day of Week', max_length=5, initial='*')

    scan_type = forms.ChoiceField(label='Scan Type', choices=ScanForm.SCAN_CHOICES)
    ports = forms.ChoiceField(label='Ports', choices=ScanForm.PORT_CHOICES)
    ips = forms.ChoiceField(label='IPs')
    
    __cron_time = None

    def is_valid(self) -> bool:
        is_valid = super().is_valid() 
        
        minute = self.cleaned_data.get('minute')
        hour = self.cleaned_data.get('hour')
        day_of_month = self.cleaned_data.get('day_of_month')
        month = self.cleaned_data.get('month')
        day_of_week = self.cleaned_data.get('day_of_week')
        ## Ensure only numbers * , - or / are used
        cron_valid = all([c.isdigit() or c in ['*', ',', '-', '/'] for c in minute]) and \
            all([c.isdigit() or c in ['*', ',', '-', '/'] for c in hour]) and \
            all([c.isdigit() or c in ['*', ',', '-', '/'] for c in day_of_month]) and \
            all([c.isdigit() or c in ['*', ',', '-', '/'] for c in month]) and \
            all([c.isdigit() or c.lower() in ['*', ',', '-', '/', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] for c in day_of_week])
                    
        return is_valid and cron_valid

    def clean(self):
        cleaned_data = super().clean()
        minute = cleaned_data.get('minute')
        hour = cleaned_data.get('hour')
        day_of_month = cleaned_data.get('day_of_month')
        month = cleaned_data.get('month')
        day_of_week = cleaned_data.get('day_of_week')

        self.__cron_time = f"{minute} {hour} {day_of_month} {month} {day_of_week}"
        try:
            CronTrigger.from_crontab(self.__cron_time)
        except ValueError:
            raise forms.ValidationError("Invalid cron format")

        return cleaned_data
    
    def cron(self):
        return CronTrigger.from_crontab(self.__cron_time)

    def __init__(self, user, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['ips'].choices = self.get_ip_choices(user)

    def get_ip_choices(self, user):
        # Retrieve the list of IPs based on the current user
        ips = Ip.objects.filter(user=user)
        choices = [(ip.ip_id, f"{ip.alias} - {ip.ip_address}") for ip in ips]
        return choices

    def has_ips(self):
        return len(self.fields['ips'].choices) > 0