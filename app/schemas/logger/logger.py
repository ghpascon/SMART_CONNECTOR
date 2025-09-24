import json
import logging
import os
import sys
import asyncio
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path


class LoggerManager:
    def __init__(self):
        self.log_dir = None
        self.logs = deque(maxlen=100)

    def load(self):
        # --- Config ---
        self.STORAGE_DAYS = 1
        self.LOG_PATH = "Logs"
        if os.path.exists("config/actions.json"):
            with open("config/actions.json", "r") as f:
                actions_data = json.load(f)
                self.STORAGE_DAYS = actions_data.get("STORAGE_DAYS", 1)
                self.LOG_PATH = actions_data.get("LOG_PATH", "Logs")

        # --- Log directory ---
        self.log_dir = Path(self.LOG_PATH)
        self.log_dir.mkdir(exist_ok=True)

        log_filename = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

        # --- Main logger ---
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Remove old handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # --- File handler ---
        file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # --- Console handler ---
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # --- Memory handler (self.logs) ---
        def memory_emit(record):
            log_entry = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s").format(
                record
            )
            self.on_log(log_entry)

        memory_handler = logging.Handler()
        memory_handler.emit = memory_emit
        logger.addHandler(memory_handler)

        logger.info(f"LOG_FILE -> {log_filename}")

        # === Capture unhandled exceptions ===
        sys.excepthook = self.handle_exception

        # === Capture unhandled asyncio exceptions ===
        try:
            loop = asyncio.get_event_loop()
            loop.set_exception_handler(self.asyncio_exception_handler)
        except RuntimeError:
            # No running loop yet
            pass

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Capture unhandled exceptions in normal code"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow Ctrl+C to exit normally
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    def asyncio_exception_handler(self, loop, context):
        """Capture unhandled exceptions in asyncio tasks"""
        exception = context.get("exception")
        if exception:
            logging.error("Unhandled asyncio exception", exc_info=exception)
        else:
            logging.error(f"Unhandled asyncio error: {context.get('message')}")

    async def clear_old_logs(self):
        cutoff_date = datetime.now() - timedelta(days=self.STORAGE_DAYS)
        for log_path in self.log_dir.glob("*.log"):
            try:
                log_date = datetime.strptime(log_path.stem, "%Y-%m-%d")
                if log_date < cutoff_date:
                    log_path.unlink()
            except ValueError:
                continue  # Ignore files outside expected pattern
            except Exception as e:
                logging.error(f"Error removing log {log_path.name}: {e}")

    def on_log(self, message: str):
        """Add log entry to memory (deque)"""
        self.logs.appendleft(message)


# --- Global instance ---
logger_manager = LoggerManager()
