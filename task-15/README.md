# Event-Driven Microservice with CQRS and Event Sourcing

This project is a backend system built in Python that demonstrates how modern applications handle data using **CQRS (Command Query Responsibility Segregation)** and **Event Sourcing**.

## What This Project Does

The system processes an order lifecycle using an event-driven approach:

* A command is issued to create an order
* The system generates events instead of directly storing state
* Events are stored in an append-only event store
* Event handlers process these events asynchronously
* A separate read model is updated for fast queries
* The system can reconstruct the entire state from stored events

## Core Concepts Used

### 1. CQRS (Command Query Responsibility Segregation)

The system separates:

* **Command side (write operations):** Handles business logic and generates events
* **Query side (read operations):** Reads from a precomputed, optimized data model

### 2. Event Sourcing

Instead of storing the latest state, the system stores all changes as events:

* Every action (order placed, updated, paid, shipped) is recorded as an event
* The current state is derived by replaying these events

### 3. Event-Driven Architecture

Events are published to a message bus and handled asynchronously:

* One event can trigger multiple independent handlers
* Examples: updating dashboards, sending emails, updating analytics

### 4. Eventual Consistency

The read model is updated asynchronously, meaning:

* The write and read sides are not instantly synchronized
* The system becomes consistent after event processing

## Workflow

1. **Place Order Command**

   * Creates an order aggregate
   * Emits events like `OrderPlaced` and `InventoryReserved`

2. **Event Processing**

   * Handlers update the read model
   * Notifications and analytics are triggered

3. **Order Lifecycle Events**

   * OrderUpdated
   * PaymentProcessed
   * OrderShipped

4. **Query Side**

   * Reads from a denormalized store for fast response

5. **Event Replay**

   * Rebuilds the order state from stored events
   * Enables auditing and debugging

## output

```txt
python main.py
[WRITE] PlaceOrderCommand received
[WRITE] Order ORD-993D77 created
[EVENT STORE] Appended 3 events
[BUS] Publishing events...
[HANDLER] Updating Read Model...
[HANDLER] Revenue updated: 239.96
[HANDLER] Email sent to C-42
[EVENT STORE] Appended 1 events
[EVENT STORE] Appended 1 events
[EVENT STORE] Appended 1 events

=== QUERY RESULT ===
{'order_id': 'ORD-993D77', 'customer_id': 'C-42', 'status': 'PLACED', 'total': 239.96, 'item_count': 4, 'placed_at': '2026-04-12T17:09:51.578997'}

=== EVENT REPLAY ===
[Event #1] {'type': 'OrderPlaced', 'order_id': 'ORD-993D77', 'customer': 'C-42', 'total': 239.96, 'items': 4, 'timestamp': '2026-04-12T17:09:51.578997'}
[Event #2] {'type': 'InventoryReserved', 'sku': 'WIDGET-01', 'qty': 3}
[Event #3] {'type': 'InventoryReserved', 'sku': 'GADGET-05', 'qty': 1}
[Event #4] {'type': 'OrderUpdated', 'order_id': 'ORD-993D77', 'new_total': 89.97, 'timestamp': '2026-04-12T17:09:51.696269'}
[Event #5] {'type': 'PaymentProcessed', 'order_id': 'ORD-993D77', 'amount': 89.97, 'method': 'card_ending_4242', 'timestamp': '2026-04-12T17:09:51.698046'}
[Event #6] {'type': 'OrderShipped', 'order_id': 'ORD-993D77', 'tracking': '1Z999AA10123456784', 'timestamp': '2026-04-12T17:09:51.698046'}

Reconstructed State: {'id': 'ORD-993D77', 'status': 'SHIPPED', 'total': 89.97, 'items': 3}  
PS E:\Intern\python\task-15> python main.py
[WRITE] PlaceOrderCommand received
[WRITE] Order ORD-FE3E93 created
[EVENT STORE] Appended 3 events
[BUS] Publishing events...
[HANDLER] Revenue updated: 239.96
[HANDLER] Email sent to C-42
[EVENT STORE] Appended 1 events
[EVENT STORE] Appended 1 events
[EVENT STORE] Appended 1 events

=== QUERY RESULT ===
{'order_id': 'ORD-FE3E93', 'customer_id': 'C-42', 'status': 'SHIPPED', 'total': 89.97, 'item_count': 3, 'placed_at': '2026-04-12T17:11:30.613935'}

=== EVENT REPLAY ===
[Event #1] {'type': 'OrderPlaced', 'order_id': 'ORD-FE3E93', 'customer': 'C-42', 'total': 239.96, 'items': 4, 'timestamp': '2026-04-12T17:11:30.613935'}
[Event #2] {'type': 'InventoryReserved', 'sku': 'WIDGET-01', 'qty': 3}
[Event #3] {'type': 'InventoryReserved', 'sku': 'GADGET-05', 'qty': 1}
[Event #4] {'type': 'OrderUpdated', 'order_id': 'ORD-FE3E93', 'new_total': 89.97, 'timestamp': '2026-04-12T17:11:30.718688'}
[Event #5] {'type': 'PaymentProcessed', 'order_id': 'ORD-FE3E93', 'amount': 89.97, 'method': 'card_ending_4242', 'timestamp': '2026-04-12T17:11:30.718688'}
[Event #6] {'type': 'OrderShipped', 'order_id': 'ORD-FE3E93', 'tracking': '1Z999AA10123456784', 'timestamp': '2026-04-12T17:11:30.718688'}

Reconstructed State: {'id': 'ORD-FE3E93', 'status': 'SHIPPED', 'total': 89.97, 'items': 3}
```

## Key Characteristics

* Append-only event storage
* Fully traceable system history
* Scalable read and write separation
* Asynchronous processing using `asyncio`
* Modular and extensible design

## Summary

This project simulates how real-world distributed systems (e.g., e-commerce platforms) manage data reliably and scalably using event-driven patterns, CQRS, and event sourcing.
