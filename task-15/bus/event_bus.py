from collections import defaultdict
import asyncio

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)

    async def publish(self, events):
        tasks = []
        for event in events:
            handlers = self.subscribers[event["type"]]
            for handler in handlers:
                tasks.append(handler(event))
        await asyncio.gather(*tasks)