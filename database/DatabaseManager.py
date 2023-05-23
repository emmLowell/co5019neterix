from os import getenv
from typing import Any, AsyncGenerator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from website.Scanner.models import Schedule



from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import ConfigManager, GeneralConfig

from .SQLQueries import CREATE_TABLES, SQL_TABLE_EXISTS, SQLITE_TABLE_EXISTS, Tables
from django.conf import settings
import django
import asyncio


class Dialect:
    SQLITE = "sqlite"
    MYSQL = "mysql"


class DatabaseManager:
    config: ConfigManager
    DB_URL: str = getenv("DB_URL", "sqlite+aiosqlite:///./database.db")
    DEBUG: bool = bool(getenv("DEBUG", "false").lower() == "true")
    session_maker: async_sessionmaker[AsyncSession] = None
    async_engine: AsyncEngine
    dialect: Dialect = Dialect.SQLITE

    def __init__(self, config: ConfigManager):
        self.config = config
        general_config = self.config.read_config(GeneralConfig)
        if general_config.production:
            from website.Neterix import settings as websettings
        else:
            from website.Neterix import settings_dev as websettings
        settings.configure(
            DATABASES=websettings.DATABASES,
            INSTALLED_APPS=["website.Scanner.apps.ScannerConfig"],
        )
        django.setup()

    def get_schedules(self) -> List['Schedule']:
        from website.Scanner.models import Schedule
        return Schedule.objects.all()

        

    def create_engine(self) -> AsyncEngine:
        if "aiomysql" in DatabaseManager.DB_URL:
            from aiomysql.sa import create_engine

            self.async_engine = create_async_engine(
                DatabaseManager.DB_URL,
                echo=DatabaseManager.DEBUG,
                asyncio_engine_strategy=create_engine,
            )
            self.dialect = Dialect.MYSQL
        else:
            self.async_engine = create_async_engine(DatabaseManager.DB_URL, echo=True)
            self.dialect = Dialect.SQLITE
        return self.async_engine

    def create_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        self.session_maker = async_sessionmaker(
            self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        return self.session_maker

    def generate_session(
        self, auto_commit: bool = False
    ) -> AsyncGenerator[AsyncSession, None]:
        if not self.session_maker:
            self.create_engine()
            self.create_sessionmaker()

        if auto_commit:
            return self.session_maker.begin()
        else:
            return self.session_maker()

    async def check_db(self):
        async with self.generate_session() as session:
            session: AsyncSession = session
            print(await session.execute(text("SELECT 1")))
        await self.check_tables()

    async def __create_table(self, table: Tables, cursor: AsyncSession):
        return await cursor.execute(text(CREATE_TABLES[table]))

    async def __tables_exists(self, table: Tables, cursor: AsyncSession):
        query = await cursor.execute(
            text(SQL_TABLE_EXISTS)
            if self.dialect == Dialect.MYSQL
            else text(SQLITE_TABLE_EXISTS),
            {"table_name": table.value[1]},
        )

        result = query.scalar_one_or_none()
        return result

    async def check_tables(self):
        tables = Tables.__members__.values()
        session = self.generate_session(auto_commit=True)
        async with session as cursor:
            results = {
                table: await self.__tables_exists(table, cursor) for table in tables
            }
            for table, result in results.items():
                if result is None:
                    await self.__create_table(table, cursor)
