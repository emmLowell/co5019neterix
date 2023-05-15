import asyncio

from database import DatabaseManager

from dotenv import load_dotenv

load_dotenv()

class Main:
    database: DatabaseManager

    async def start(self):
        self.database = DatabaseManager()
        await self.database.check_db()


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.start())
