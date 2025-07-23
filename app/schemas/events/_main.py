import asyncio

import logging
from .actions import Actions
from .on_event import OnEvent

from collections import deque


class Events(OnEvent, Actions):
    def __init__(self):
        self.tags = {}
        self.events = deque(maxlen=20)
        self.actions = {}
        asyncio.run(self.set_actions(None))

    async def clear_tags(self, device: str | None = None):
        if device is None:
            self.tags = {}
            return
        self.tags = {k: v for k, v in self.tags.items() if v.get("device") != device}
        logging.info(f"[ CLEAR ] -> Reader: {device}")


events = Events()
