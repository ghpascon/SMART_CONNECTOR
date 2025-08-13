import asyncio
from datetime import datetime, timedelta, timezone
from app.schemas.logger import logger_manager
import logging

from app.core.config import settings
from app.db.database import database_engine
from app.schemas.devices import devices
from app.schemas.events import events

async def connect_devices():
    await devices.create_connect_loop()

async def periodic_clear_tags():
    while True:
        interval = settings.data.get("CLEAR_OLD_TAGS_INTERVAL", 0)
        try:
            interval = int(interval)
        except (ValueError, TypeError):
            interval = 0

        await asyncio.sleep(interval if interval > 0 else 10)

        if interval > 0:
            now = datetime.now()
            expired_keys = []
            for key, value in list(events.tags.items()):
                timestamp = value.get("timestamp")
                if timestamp and isinstance(timestamp, datetime):
                    if now - timestamp > timedelta(seconds=interval):
                        expired_keys.append(key)
            for key in expired_keys:
                del events.tags[key]
                logging.info(f"[ TAG REMOVED ] - {key}")


async def daily_clear_db():
    while True:
        await logger_manager.clear_old_logs()
        await database_engine.clear_db(settings.data.get("STORAGE_DAYS"))

        # Calcula a próxima meia-noite em horário de Brasília (UTC-3)
        now = datetime.now(timezone(timedelta(hours=-3)))
        next_run = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        wait_seconds = (next_run - now).total_seconds()

        logging.info(
            f"Next DB clear scheduled in {wait_seconds/3600:.2f} hours (Brasília time)"
        )
        await asyncio.sleep(wait_seconds)
