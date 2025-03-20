from flask import Flask, request, jsonify
import joblib
import numpy as np
import json

app = Flask(__name__)

model_1 = joblib.load('model_1.pkl')
model_2 = joblib.load('model_2.pkl')
model_3 = joblib.load('model_3.pkl')

with open('model_balances.json', 'r') as f:
    model_balances = json.load(f)

def update_model_balance(model_id, correct_prediction):
    if correct_prediction:
    
        model_balances[model_id]["incorrect_predictions"] = 0  
    else:
       
        model_balances[model_id]["incorrect_predictions"] += 1
        if model_balances[model_id]["incorrect_predictions"] >= 3:
           
            model_balances[model_id]["balance"] -= 200 

   
    with open('model_balances.json', 'w') as f:
        json.dump(model_balances, f)


@app.route('/predict', methods=['GET'])
def predict():
    sepal_length = float(request.args.get('sepal_length'))
    sepal_width = float(request.args.get('sepal_width'))
    petal_length = float(request.args.get('petal_length'))
    petal_width = float(request.args.get('petal_width'))

    models = [model_1, model_2, model_3]
    model_ids = ['model_1', 'model_2', 'model_3']
    predictions = []

    for i, model in enumerate(models):
        prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        correct_prediction = (prediction[0] == 1) 
        predictions.append(prediction[0])

        update_model_balance(model_ids[i], correct_prediction)

    group_prediction = np.mean(predictions)

    return jsonify({'group_prediction': group_prediction})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

