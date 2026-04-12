class UpdateOrderCommand:
    def __init__(self, order_id, removed_item_price):
        self.order_id = order_id
        self.removed_item_price = removed_item_price