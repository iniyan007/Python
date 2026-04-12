class ReadStore:
    def __init__(self):
        self.orders = {}

    def insert_order(self, data):
        self.orders[data["order_id"]] = data

    def get_order(self, order_id):
        return self.orders.get(order_id)


read_store = ReadStore()