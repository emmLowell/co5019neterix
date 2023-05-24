from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from website.Scanner.models import Schedule, Port, Ip

import django
from django.conf import settings

from config import ConfigManager, GeneralConfig


class DatabaseManager:
    config: ConfigManager

    def __init__(self, config: ConfigManager):
        self.config = config
        general_config = self.config.read_config(GeneralConfig)
        if general_config.production:
            from website.Neterix import settings as websettings
        else:
            from website.Neterix import settings_dev as websettings
        settings.configure(
            DATABASES=websettings.DATABASES,
            INSTALLED_APPS=['django.contrib.auth','django.contrib.contenttypes',"website.Scanner.apps.ScannerConfig"]
        )
        django.setup()

    def get_schedules(self) -> List['Schedule']:
        from website.Scanner.models import Schedule
        return Schedule.objects.all()

    def get_previous_ports(self, ip: 'Ip') -> Optional[List['Port']]:
        from website.Scanner.models import Port, Scan
        scan = Scan.get_latest_scan(ip)
        if scan is None: return None
        return Port.objects.filter(scan=scan)