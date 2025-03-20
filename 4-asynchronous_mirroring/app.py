from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Base de données en mémoire simulée
products_db = {}
orders_db = {}

# Fonction pour charger les produits depuis la "base de données" en mémoire
def get_products():
    return list(products_db.values())

# Fonction pour ajouter un produit à la "base de données" en mémoire
def add_product_to_db(product):
    product_id = len(products_db) + 1  # Assigner un ID unique
    products_db[product_id] = product
    return product_id

# Fonction pour ajouter une commande à la "base de données" en mémoire
def add_order_to_db(order):
    order_id = len(orders_db) + 1  # Assigner un ID unique
    orders_db[order_id] = order
    return order_id

# File d'attente pour la réplication des données
replication_queue = []

# Fonction pour mettre les données à répliquer dans la file d'attente
def queue_replication(data):
    replication_queue.append(data)

# Fonction pour traiter la file d'attente et répliquer les données
def replicate_data():
    while True:
        if replication_queue:
            data = replication_queue.pop(0)
            # Simuler la réplique vers une base miroir en mémoire
            print("Data replicated:", data)
        time.sleep(5)  # Attendre 5 secondes avant de vérifier à nouveau la file d'attente

# Lancer la réplication en arrière-plan
def start_replication_thread():
    thread = threading.Thread(target=replicate_data)
    thread.daemon = True  # Permet au thread de se terminer lorsqu'on arrête l'application
    thread.start()

# Route pour obtenir tous les produits
@app.route('/products', methods=['GET'])
def get_all_products():
    products = get_products()
    return jsonify(products)

# Route pour ajouter un produit
@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    product_id = add_product_to_db(new_product)
    queue_replication(new_product)
    return jsonify({"id": product_id, **new_product}), 201

# Route pour ajouter une commande
@app.route('/orders', methods=['POST'])
def add_order():
    new_order = request.get_json()
    order_id = add_order_to_db(new_order)
    queue_replication(new_order)
    return jsonify({"id": order_id, **new_order}), 201

# Simuler une panne (failover)
@app.route('/simulate_failover', methods=['POST'])
def simulate_failover():
    # Simuler un failover en répliquant les données vers un miroir en mémoire
    print("Failover successfully simulated.")
    return jsonify({"message": "Failover successfully simulated."}), 200

if __name__ == '__main__':
    # Démarrer le thread de réplication en arrière-plan
    start_replication_thread()
    app.run(debug=True)
