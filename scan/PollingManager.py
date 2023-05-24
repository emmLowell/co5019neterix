from typing import List, TYPE_CHECKING
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from config import ConfigManager
from database import DatabaseManager
from scan import NmapScanner, VulnersScanner
from django.utils import timezone
from threading import Thread

import traceback


if TYPE_CHECKING:
    from website.Scanner.models import Schedule, Ip, Cve

class PollingManager:
    database: DatabaseManager
    scheduler: BackgroundScheduler
    config_manager: ConfigManager
    
    __jobs = {}

    def __init__(self, database: DatabaseManager, config: ConfigManager):
        self.database = database
        self.config_manager = config
        self.scheduler = BackgroundScheduler()

    def poll_once(self, ip_id: str, scan_type: str, port_type: str):
        from website.Scanner.models import Port, Scan, Ip, Cve
        if(isinstance(ip_id, str)):
            ip = Ip.objects.get(ip_id=int(ip_id))
        elif(isinstance(ip_id, Ip)):
            ip = ip_id
        else:
            raise TypeError("ip_id must be either str or Ip")
        
        if(not port_type.isdigit()):
            port_type = None
        
        scan = Scan(ip=ip, scan_type=scan_type, os="Unknown", error=False, nmap_params=f"-sV -s{scan_type} {port_type}")
        scan.save()
        error = False
        update_fields = ["end_time"]
        ports = []
        try:
            nmap_scan = NmapScanner.scan(ip.ip_address, options=f"-s{scan_type}", top_ports=port_type)
            
            new_port_details = nmap_scan.all_ports()
        
            ports.extend(Port.objects.bulk_create(
                [Port(scan=scan, port_number=int(port.portid), service=port.service.product, version=port.service.version) for port in new_port_details]
            ))
            
            update_fields.append("nmap_params")
            scan.nmap_params = nmap_scan.stats.args
        except Exception as e:
            print(e)
            scan.error = True
            error = True
        
        try:
            vulners = VulnersScanner()
            
            vulnerabilties = []
            
            for port in ports:
                results = vulners.find_all_exploits(port.service, port.version)
                vulnerabilties.extend(results)
                for result in results:
                    for cve in result.cvelist:
                        Cve(port=port, scan=scan, cve=cve).save()
            
        except Exception as e:
            traceback.print_exc()
            print(e)
            scan.error = True
            error = True
            
        scan.end_time = timezone.now()
        if(error):
            update_fields.append("error")
        scan.save(update_fields=update_fields)

        ## Compare old ports to new ports
        if(error):return
        old_port_details = self.database.get_previous_ports(ip)
        
        if(old_port_details is None or len(old_port_details) <= 0):return
        
        new_ports = [int(port.portid) for port in new_port_details]
        old_ports = [int(port.port_number) for port in old_port_details]
        
        new_open_ports = set(new_ports).difference(old_ports)
        new_closed_ports = set(old_ports).difference(new_ports)
        
        if(len(new_open_ports) > 0):
            print(f"New open ports: {new_open_ports}")
        if(len(new_closed_ports) > 0):
            print(f"New closed ports: {new_closed_ports}")
            
        print("Vulnerabilities",vulnerabilties)
        #TODO - report data

    def start_polling_id_once(self, ip: str, scan_type: str, port_type: str):
        print(f"Polling once. {ip}, {scan_type}, {port_type}")
        self.poll_once(ip, scan_type, port_type)

    def schedule_callback(self, schedule: 'Schedule'):
        def callback():
            thread = Thread(target=self.poll_once, args=(schedule.ip, schedule.scan_type, schedule.port_type))
            thread.start()
        return callback

    def schedule_task(self, schedule: 'Schedule'):
        cron_trigger = CronTrigger.from_crontab(schedule.cron_time)
        job = self.scheduler.add_job(
            func=self.schedule_callback(schedule),
            trigger=cron_trigger
        )
        self.__jobs[schedule.id] = job

    def start_polling(self):
        # load all ips from database and add them to scheduler        
        schedules: List['Schedule']= self.database.get_schedules()
        for schedule in schedules:
            self.schedule_task(schedule)
        self.scheduler.start()
        
    def stop_polling(self, schedule_id: str):
        schedule_id = int(schedule_id)
        if(schedule_id not in self.__jobs):return
        job = self.__jobs[schedule_id]
        del self.__jobs[schedule_id]
        job.remove()
        
    def start_polling_id(self, schedule_id: str):
        from website.Scanner.models import Schedule
        try:
            schedule = Schedule.objects.get(id=int(schedule_id))
        except Schedule.DoesNotExist: 
            return
        self.schedule_task(schedule)
    
        
        
