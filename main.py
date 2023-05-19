import asyncio
from os import getenv

from database import DatabaseManager
from website import run_server
from argparse import ArgumentParser, REMAINDER
from scan import NmapScanner

from dotenv import load_dotenv

load_dotenv()


class Main:
    development = getenv("PRODUCTION", "false").lower() == "false"
    database: DatabaseManager

    async def start(self):
        self.database = DatabaseManager()

        if self.development:
            await self.run_development()
        else:
            await self.run_production()

    async def run_production(self):
        ...

    # TODO - Implement production code

    ## TODO - Process
    #   - 1. Get all ips from database
    #   - 2. Scan all ips
    #   - 3. Get all services from ips
    #   - 4. Get all products from services
    #   - 5. Save all products to database
    #   - 6. Compare?
    #   - 7. Repeat every 24 hours

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
        asyncio.run(main.start(args.debug))
    else:
        run_server(args.args)
