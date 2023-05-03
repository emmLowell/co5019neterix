import asyncio

from database import DatabaseManager


class Main:
    database: DatabaseManager

    async def start(self):
        self.database = DatabaseManager()
        await self.database.check_db()


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.start())
