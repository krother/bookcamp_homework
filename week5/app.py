
from flask import Flask, jsonify, request
from predict import get_prediction

app = Flask('Churn Predictor')

@app.route('/')
def predict():
    data = {
        'contract': request.args['contract'],
        'tenure': int(request.args['tenure']),
        'monthlycharges': float(request.args['monthlycharges'])
    }
    result = get_prediction(data)
    return jsonify({'churn_proba': result})

@app.route('/test')
def test():
    return 'hello world'
