from flask import Flask, request, jsonify
import joblib
import numpy as np
import json

app = Flask(__name__)

# Charger les modèles
model_1 = joblib.load('model_1.pkl')
model_2 = joblib.load('model_2.pkl')
model_3 = joblib.load('model_3.pkl')

# Charger les balances et performances des modèles
with open('model_balances.json', 'r') as f:
    model_balances = json.load(f)

# Fonction pour mettre à jour les performances et les balances des modèles
def update_model_balance(model_id, correct_prediction):
    if correct_prediction:
        # Le modèle a fait une prédiction correcte, pas de slashing
        model_balances[model_id]["incorrect_predictions"] = 0  # Réinitialiser les erreurs
    else:
        # Le modèle a fait une prédiction incorrecte, on applique le slashing
        model_balances[model_id]["incorrect_predictions"] += 1
        if model_balances[model_id]["incorrect_predictions"] >= 3:
            # Après 3 erreurs consécutives, slashing
            model_balances[model_id]["balance"] -= 200  # Perdre 200 euros par erreur

    # Enregistrer les modifications dans le fichier JSON
    with open('model_balances.json', 'w') as f:
        json.dump(model_balances, f)

# Route pour faire une prédiction et appliquer le slashing
@app.route('/predict', methods=['GET'])
def predict():
    # Récupérer les paramètres depuis l'URL
    sepal_length = float(request.args.get('sepal_length'))
    sepal_width = float(request.args.get('sepal_width'))
    petal_length = float(request.args.get('petal_length'))
    petal_width = float(request.args.get('petal_width'))

    # Liste des modèles de groupe et de leurs identifiants
    models = [model_1, model_2, model_3]
    model_ids = ['model_1', 'model_2', 'model_3']
    predictions = []

    # Faire des prédictions et appliquer le slashing en fonction des erreurs
    for i, model in enumerate(models):
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        correct_prediction = (prediction[0] == 1)  # Exemple : 1 est la classe correcte
        predictions.append(prediction[0])

        # Mettre à jour le solde du modèle basé sur la performance
        update_model_balance(model_ids[i], correct_prediction)

    # Calculer la moyenne des prédictions (consensus)
    group_prediction = np.mean(predictions)

    # Retourner la prédiction du groupe en format JSON
    return jsonify({'group_prediction': group_prediction})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

