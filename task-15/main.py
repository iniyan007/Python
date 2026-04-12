import asyncio

from commands.place_order import PlaceOrderCommand
from commands.update_order import UpdateOrderCommand
from commands.process_payment import ProcessPaymentCommand
from commands.ship_order import ShipOrderCommand
from aggregates.order import OrderAggregate
from events.event_store import EventStore
from bus.event_bus import EventBus
from bus.command_bus import CommandBus

from handlers.order_projection import order_dashboard_projection
from handlers.notification import notification_service
from handlers.analytics import analytics_projection

from queries.get_order import get_order_summary
from aggregates.order import OrderAggregate

async def main():
    event_store = EventStore()
    event_bus = EventBus()


    event_bus.subscribe("OrderPlaced", order_dashboard_projection)
    event_bus.subscribe("OrderPlaced", notification_service)
    event_bus.subscribe("OrderPlaced", analytics_projection)
    event_bus.subscribe("OrderUpdated", order_dashboard_projection)
    event_bus.subscribe("PaymentProcessed", order_dashboard_projection)
    event_bus.subscribe("OrderShipped", order_dashboard_projection)

    command_bus = CommandBus(event_store, event_bus)


    cmd = PlaceOrderCommand(
        customer_id="C-42",
        items=[
            {"sku": "WIDGET-01", "qty": 3, "price": 29.99},
            {"sku": "GADGET-05", "qty": 1, "price": 149.99}
        ]
    )

    order_id = await command_bus.dispatch(cmd)
    aggregate = OrderAggregate()
    update_events = aggregate.update_order(order_id, 89.97)
    event_store.append(order_id, update_events)
    await event_bus.publish(update_events)

    payment_events = aggregate.process_payment(order_id, 89.97)
    event_store.append(order_id, payment_events)
    await event_bus.publish(payment_events)

    ship_events = aggregate.ship_order(order_id)
    event_store.append(order_id, ship_events)
    await event_bus.publish(ship_events)
    
    print("\n=== QUERY RESULT ===")
    result = get_order_summary(order_id)
    print(result)

    print("\n=== EVENT REPLAY ===")
    events = event_store.get_events(order_id)
    for i, e in enumerate(events):
        print(f"[Event #{i+1}] {e}")

    rebuilt = event_store.replay(order_id)
    print("\nReconstructed State:", rebuilt)


if __name__ == "__main__":
    asyncio.run(main())