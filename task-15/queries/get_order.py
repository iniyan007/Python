from read_model.read_store import read_store

def get_order_summary(order_id):
    return read_store.get_order(order_id)