from flask import Flask, request, jsonify
import json
import shutil

app = Flask(__name__)

# Fonction pour charger les produits depuis le stockage principal ou miroir
def load_products(primary=True):
    filename = 'products_primary.json' if primary else 'products_mirror.json'
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas, on retourne une liste vide
        return []

# Fonction pour sauvegarder les produits dans le stockage principal et miroir
def save_products(products):
    try:
        # Sauvegarde dans le stockage principal
        with open('products_primary.json', 'w') as f:
            json.dump(products, f, indent=4)
        
        # Sauvegarde dans le stockage miroir
        with open('products_mirror.json', 'w') as f:
            json.dump(products, f, indent=4)
    except Exception as e:
        print(f"Error saving products: {e}")

# Fonction pour charger les commandes depuis le stockage principal ou miroir
def load_orders(primary=True):
    filename = 'orders_primary.json' if primary else 'orders_mirror.json'
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas, on retourne une liste vide
        return []

# Fonction pour sauvegarder les commandes dans le stockage principal et miroir
def save_orders(orders):
    try:
        # Sauvegarde dans le stockage principal
        with open('orders_primary.json', 'w') as f:
            json.dump(orders, f, indent=4)
        
        # Sauvegarde dans le stockage miroir
        with open('orders_mirror.json', 'w') as f:
            json.dump(orders, f, indent=4)
    except Exception as e:
        print(f"Error saving orders: {e}")

# Route pour afficher tous les produits
@app.route('/products', methods=['GET'])
def get_products():
    products = load_products()
    return jsonify(products)

# Route pour ajouter un produit
@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    products = load_products()
    new_product['id'] = len(products) + 1  # Assigner un ID unique
    products.append(new_product)
    
    # Sauvegarde des produits dans les deux systèmes de stockage (principal et miroir)
    save_products(products)
    
    return jsonify(new_product), 201

# Route pour afficher toutes les commandes
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = load_orders()
    return jsonify(orders)

# Route pour ajouter une commande
@app.route('/orders', methods=['POST'])
def add_order():
    new_order = request.get_json()
    orders = load_orders()
    new_order['id'] = len(orders) + 1
    orders.append(new_order)
    
    # Sauvegarde des commandes dans les deux systèmes de stockage (principal et miroir)
    save_orders(orders)
    
    return jsonify(new_order), 201

# Fonction pour effectuer un test de panne simulée (failover)
@app.route('/simulate_failover', methods=['POST'])
def simulate_failover():
    try:
        # Simuler une défaillance en copiant les données du principal vers le miroir
        shutil.copy('products_primary.json', 'products_mirror.json')
        shutil.copy('orders_primary.json', 'orders_mirror.json')
        return jsonify({"message": "Failover successfully simulated."}), 200
    except Exception as e:
        return jsonify({"error": f"Failover failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
