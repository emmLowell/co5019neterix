from django import forms
from .models import Schedule
from apscheduler.triggers.cron import CronTrigger

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def clean_cron_time(self):
        cron_time = self.cleaned_data.get('cron_time')

        try:
            CronTrigger.from_crontab(cron_time)
        except ValueError:
            raise forms.ValidationError("Invalid cron format")

        return cron_time
