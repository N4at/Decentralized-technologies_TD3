from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

products_db = {}
orders_db = {}

def get_products():
    return list(products_db.values())

def add_product_to_db(product):
    product_id = len(products_db) + 1 
    products_db[product_id] = product
    return product_id

def add_order_to_db(order):
    order_id = len(orders_db) + 1 
    orders_db[order_id] = order
    return order_id

replication_queue = []

def queue_replication(data):
    replication_queue.append(data)

def replicate_data():
    while True:
        if replication_queue:
            data = replication_queue.pop(0)
            print("Data replicated:", data)
        time.sleep(5)  

def start_replication_thread():
    thread = threading.Thread(target=replicate_data)
    thread.daemon = True  
    thread.start()

@app.route('/products', methods=['GET'])
def get_all_products():
    products = get_products()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    product_id = add_product_to_db(new_product)
    queue_replication(new_product)
    return jsonify({"id": product_id, **new_product}), 201

@app.route('/orders', methods=['POST'])
def add_order():
    new_order = request.get_json()
    order_id = add_order_to_db(new_order)
    queue_replication(new_order)
    return jsonify({"id": order_id, **new_order}), 201

@app.route('/simulate_failover', methods=['POST'])
def simulate_failover():
    print("Failover successfully simulated.")
    return jsonify({"message": "Failover successfully simulated."}), 200

if __name__ == '__main__':
    start_replication_thread()
    app.run(debug=True)
