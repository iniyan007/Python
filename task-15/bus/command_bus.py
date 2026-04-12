from aggregates.order import OrderAggregate

class CommandBus:
    def __init__(self, event_store, event_bus):
        self.event_store = event_store
        self.event_bus = event_bus

    async def dispatch(self, command):
        print("[WRITE] PlaceOrderCommand received")

        aggregate = OrderAggregate()
        order_id, events = aggregate.place_order(command)

        self.event_store.append(order_id, events)

        print("[BUS] Publishing events...")
        await self.event_bus.publish(events)

        return order_id