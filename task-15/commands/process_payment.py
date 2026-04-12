class ProcessPaymentCommand:
    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount