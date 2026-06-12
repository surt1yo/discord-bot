import aiosqlite
import os


class Database:
    def __init__(self, path):
        self.path = path
        self.db = None

    async def connect(self):
        # Create data folder automatically
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        self.db = await aiosqlite.connect(self.path)

    async def init(self):
        await self.db.executescript("""
        CREATE TABLE IF NOT EXISTS afk(
            user_id INTEGER PRIMARY KEY,
            reason TEXT,
            started TEXT,
            mentions INTEGER DEFAULT 0,
            links TEXT
        );

        CREATE TABLE IF NOT EXISTS blacklist(
            user_id INTEGER PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS whitelist(
            user_id INTEGER PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS commands(
            name TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        );
        """)
        await self.db.commit()

    async def execute(self, query, args=()):
        await self.db.execute(query, args)
        await self.db.commit()

    async def fetchone(self, query, args=()):
        async with self.db.execute(query, args) as cursor:
            return await cursor.fetchone()

    async def fetchall(self, query, args=()):
        async with self.db.execute(query, args) as cursor:
            return await cursor.fetchall()

    async def close(self):
        if self.db:
            await self.db.close()