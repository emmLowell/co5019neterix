import asyncio
from os import getenv

from database import DatabaseManager
from scan import NmapScanner

from dotenv import load_dotenv

load_dotenv()


class Main:
    development = getenv("PRODUCTION", "false").lower() == "false"
    database: DatabaseManager
    nmapScanner: NmapScanner

    async def start(self):
        self.database = DatabaseManager()
        self.nmapScanner = NmapScanner()
        await self.database.check_db()
        
        if(self.development):
            await self.run_development()
        else:
            await self.run_production()
    
    async def run_production(self):...
        #TODO - Implement production code

    async def run_development(self, test_ip: str = "127.0.0.1"):
        data = self.nmapScanner.scan(test_ip)
        print("\n".join(data.all_service_products()))


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.start())
