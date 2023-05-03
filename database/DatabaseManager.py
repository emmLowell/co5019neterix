import asyncio
from functools import wraps
from os import getenv
from typing import Any, AsyncGenerator, Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from .SQLQueries import (CREATE_TABLES, SQL_TABLE_EXISTS, SQLITE_TABLE_EXISTS,
                         Tables)


class Dialect:
    SQLITE = "sqlite"
    MYSQL = "mysql"


class DatabaseManager:
    DB_URL: str = getenv("DB_URL", "sqlite+aiosqlite:///./database.db")
    DEBUG: bool = bool(getenv("DEBUG", "false").lower() == "true")
    PRODUCTION: bool = bool(getenv("PRODUCTION", "false").lower() == "true")
    session_maker: async_sessionmaker[AsyncSession] = None
    async_engine: AsyncEngine
    dialect: Dialect = Dialect.SQLITE

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
