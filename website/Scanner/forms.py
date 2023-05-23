from django import forms

from website.Scanner.models import Ip

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

