from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from config import ConfigManager
from database import DatabaseManager


class PollingManager:
    database: DatabaseManager
    scheduler: BackgroundScheduler
    config_manager: ConfigManager

    def __init__(self, database: DatabaseManager, config: ConfigManager):
        self.database = database
        self.config_manager = config
        self.scheduler = BackgroundScheduler()

    def schedule_callback(self, ip: str):
        def callback():
            print(f"Polling {ip}")
            # TODO: - Process
            #   - 1. Get all ips from database
            #   - 2. Scan all ips
            #   - 3. Get all services from ips
            #   - 4. Get all products from services
            #   - 5. Save all products to database
            #   - 6. Compare?
            #   - 7. Repeat every 24 hours

        return callback

    def start_polling(self):
        # load all ips from database and add them to scheduler
        schedules = self.database.get_schedules()
        for schedule in schedules:
            cron_trigger = CronTrigger.from_crontab(schedule.cron_time)
            self.scheduler.add_job(
                self.schedule_callback(schedule.ip), "cron", trigger=cron_trigger
            )
        self.scheduler.start()
