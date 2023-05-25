import asyncio
import signal
import subprocess
from argparse import REMAINDER, ArgumentParser
from asyncio import Task
from signal import SIGABRT, SIGINT, SIGTERM
from signal import signal as signal_fn
from typing import Optional

from dotenv import load_dotenv

from config import ConfigManager, GeneralConfig
from database import DatabaseManager
from scan import NmapScanner, PollingManager
from website import run_server
from website.RedisManager import RedisManager


class Main:
    database: DatabaseManager
    configManager: ConfigManager = ConfigManager()
    redisManager: RedisManager
    polling: PollingManager
    is_running: bool = True

    @property
    def general_config(self) -> GeneralConfig:
        return self.configManager.read_config(GeneralConfig)

    async def start(self):
        self.database = DatabaseManager(self.configManager)
        self.polling = PollingManager(database=self.database, config=self.configManager)

        self.redisManager = RedisManager()

        self.redisManager.listen(self)

        if not self.general_config.production:
            await self.run_development()
        else:
            await self.run_production()

    async def run_production(self):
        print("Polling")
        await asyncio.to_thread(self.polling.start_polling)

        await self.idle()

    async def idle(self):
        task: Optional[Task] = None

        signals = {
            k: v for v, k in signal.__dict__.items()
            if v.startswith("SIG") and not v.startswith("SIG_")
        }

        def signal_handler(signum, __):
            print(f"Stop signal received ({signals[signum]}). Exiting...")
            if (task is None):
                return
            task.cancel()

        for s in (SIGINT, SIGTERM, SIGABRT):
            signal_fn(s, signal_handler)

        async def waiting_for_signal():
            while self.is_running:
                await asyncio.sleep(600)

            print("shutting down...")

        try:
            task = await asyncio.create_task(waiting_for_signal())
        except asyncio.CancelledError:
            pass

    async def run_development(self, test_ip: str = "127.0.0.1"):
        self.redisManager.send("scanner_tunnel", "development")
        await asyncio.to_thread(self.polling.start_polling)
        data = NmapScanner.scan(target=test_ip)
        print("\n".join(data.all_service_products()))


if __name__ == "__main__":
    print("Starting Neterix")
    load_dotenv()

    main = Main()
    parser = ArgumentParser("Neterix")
    parser.add_argument("-s", dest="scan", action="store_true")
    parser.add_argument("-d", dest="debug", action="store_true")
    parser.add_argument("-b", dest="both", action="store_true")
    parser.add_argument("--port", dest="port", type=int, default=8080)
    parser.add_argument("args", nargs=REMAINDER)

    args = parser.parse_args()

    if (args.both):  # For development old, production use ASGI or WSGI server for django
        subprocess.Popen(["python3", "main.py", "makemigrations", "Scanner"]).wait()
        subprocess.Popen(["python3", "main.py", "migrate"]).wait()
        website = subprocess.Popen(["python3", "main.py", "runserver", f"0.0.0.0:{args.port}", "--noreload"])
        background = subprocess.Popen(["python3", "main.py", "-s"])

        website.wait()
        background.wait()
    else:
        if args.scan:
            asyncio.run(main.start())
        else:
            run_server(args.args, production=main.general_config.production)
