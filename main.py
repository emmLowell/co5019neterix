import asyncio
from argparse import REMAINDER, ArgumentParser

from dotenv import load_dotenv

from config import ConfigManager, GeneralConfig
from database import DatabaseManager
from scan import NmapScanner, PollingManager
from website import run_server
load_dotenv()


class Main:
    database: DatabaseManager
    configManager: ConfigManager

    @property
    def general_config(self) -> GeneralConfig:
        return self.configManager.read_config(GeneralConfig)

    async def start(self):
        self.configManager = ConfigManager()
        #self.database = DatabaseManager(self.configManager)

        if not self.general_config.production:
            await self.run_development()
        else:
            await self.run_production()

    async def run_production(self):
        polling = PollingManager(database=self.database, config=self.configManager)
        await asyncio.to_thread(polling.start_polling)

        await asyncio.sleep(60 * 60 * 24)
        # TODO: forever sleep - ignore for now



    async def run_development(self, test_ip: str = "127.0.0.1"):
        data = NmapScanner.scan(target=test_ip)
        print("\n".join(data.all_service_products()))


if __name__ == "__main__":
    main = Main()
    parser = ArgumentParser("Neterix")
    parser.add_argument("-s", dest="scan", action="store_true")
    parser.add_argument("-d", dest="debug", action="store_true")
    parser.add_argument("args", nargs=REMAINDER)

    args = parser.parse_args()
    if args.scan:
        asyncio.run(main.start())
    else:
        run_server(args.args)
