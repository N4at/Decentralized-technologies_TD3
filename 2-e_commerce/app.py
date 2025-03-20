from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

def save_products(products):
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=4)

def load_orders():
    with open('orders.json', 'r') as f:
        return json.load(f)

def save_orders(orders):
    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=4)

def load_cart(user_id):
    try:
        with open(f'cart_{user_id}.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_cart(user_id, cart):
    with open(f'cart_{user_id}.json', 'w') as f:
        json.dump(cart, f, indent=4)

@app.route('/products', methods=['GET'])
def get_products():
    products = load_products()
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    products = load_products()
    product = next((p for p in products if p['id'] == id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    products = load_products()
    new_product['id'] = len(products) + 1  
    products.append(new_product)
    save_products(products)
    return jsonify(new_product), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    updated_data = request.get_json()
    products = load_products()
    product = next((p for p in products if p['id'] == id), None)
    if product:
        product.update(updated_data)
        save_products(products)
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    products = load_products()
    product = next((p for p in products if p['id'] == id), None)
    if product:
        products.remove(product)
        save_products(products)
        return '', 204
    return jsonify({'error': 'Product not found'}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = load_orders()
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    new_order = request.get_json()
    orders = load_orders()
    new_order['id'] = len(orders) + 1
    orders.append(new_order)
    save_orders(orders)
    return jsonify(new_order), 201

@app.route('/cart/<int:user_id>', methods=['GET'])
def view_cart(user_id):
    cart = load_cart(user_id)
    return jsonify(cart)

@app.route('/cart/<int:user_id>', methods=['POST'])
def add_to_cart(user_id):
    product_id = request.get_json().get('product_id')
    product = next((p for p in load_products() if p['id'] == product_id), None)
    if product:
        cart = load_cart(user_id)
        cart.append(product)
        save_cart(user_id, cart)
        return jsonify(cart)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/cart/<int:user_id>', methods=['DELETE'])
def remove_from_cart(user_id):
    product_id = request.get_json().get('product_id')
    cart = load_cart(user_id)
    product = next((p for p in cart if p['id'] == product_id), None)
    if product:
        cart.remove(product)
        save_cart(user_id, cart)
        return jsonify(cart)
    return jsonify({'error': 'Product not in cart'}), 404

if __name__ == '__main__':
    app.run(debug=True)
