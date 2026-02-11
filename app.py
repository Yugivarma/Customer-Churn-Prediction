"""
Customer Churn Prediction Flask Application
Uses XGBoost model for predicting customer churn
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.sav')

try:
    model = pickle.load(open(MODEL_PATH, 'rb'))
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Feature options for the form
FEATURE_OPTIONS = {
    'gender': ['Female', 'Male'],
    'Partner': ['Yes', 'No'],
    'Dependents': ['Yes', 'No'],
    'PhoneService': ['Yes', 'No'],
    'MultipleLines': ['Yes', 'No', 'No phone service'],
    'InternetService': ['DSL', 'Fiber optic', 'No'],
    'OnlineSecurity': ['Yes', 'No', 'No internet service'],
    'OnlineBackup': ['Yes', 'No', 'No internet service'],
    'DeviceProtection': ['Yes', 'No', 'No internet service'],
    'TechSupport': ['Yes', 'No', 'No internet service'],
    'StreamingTV': ['Yes', 'No', 'No internet service'],
    'StreamingMovies': ['Yes', 'No', 'No internet service'],
    'Contract': ['Month-to-month', 'One year', 'Two year'],
    'PaperlessBilling': ['Yes', 'No'],
    'PaymentMethod': ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']
}


def preprocess_input(data):
    """
    Preprocess user input to match the model's expected format.
    The model expects 19 features with label-encoded categorical variables.
    """
    # Label encoding mappings based on typical sklearn LabelEncoder ordering (alphabetical)
    label_mappings = {
        'gender': {'Female': 0, 'Male': 1},
        'Partner': {'No': 0, 'Yes': 1},
        'Dependents': {'No': 0, 'Yes': 1},
        'PhoneService': {'No': 0, 'Yes': 1},
        'MultipleLines': {'No': 0, 'No phone service': 1, 'Yes': 2},
        'InternetService': {'DSL': 0, 'Fiber optic': 1, 'No': 2},
        'OnlineSecurity': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'OnlineBackup': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'DeviceProtection': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'TechSupport': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'StreamingTV': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'StreamingMovies': {'No': 0, 'No internet service': 1, 'Yes': 2},
        'Contract': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
        'PaperlessBilling': {'No': 0, 'Yes': 1},
        'PaymentMethod': {
            'Bank transfer (automatic)': 0,
            'Credit card (automatic)': 1,
            'Electronic check': 2,
            'Mailed check': 3
        }
    }
    
    # Create feature array in the order expected by the model
    features = []
    
    # 1. gender (encoded)
    features.append(label_mappings['gender'].get(data.get('gender', 'Male'), 1))
    
    # 2. SeniorCitizen (already numeric 0/1)
    features.append(int(data.get('SeniorCitizen', 0)))
    
    # 3. Partner (encoded)
    features.append(label_mappings['Partner'].get(data.get('Partner', 'No'), 0))
    
    # 4. Dependents (encoded)
    features.append(label_mappings['Dependents'].get(data.get('Dependents', 'No'), 0))
    
    # 5. tenure (numeric)
    features.append(float(data.get('tenure', 0)))
    
    # 6. PhoneService (encoded)
    features.append(label_mappings['PhoneService'].get(data.get('PhoneService', 'Yes'), 1))
    
    # 7. MultipleLines (encoded)
    features.append(label_mappings['MultipleLines'].get(data.get('MultipleLines', 'No'), 0))
    
    # 8. InternetService (encoded)
    features.append(label_mappings['InternetService'].get(data.get('InternetService', 'DSL'), 0))
    
    # 9. OnlineSecurity (encoded)
    features.append(label_mappings['OnlineSecurity'].get(data.get('OnlineSecurity', 'No'), 0))
    
    # 10. OnlineBackup (encoded)
    features.append(label_mappings['OnlineBackup'].get(data.get('OnlineBackup', 'No'), 0))
    
    # 11. DeviceProtection (encoded)
    features.append(label_mappings['DeviceProtection'].get(data.get('DeviceProtection', 'No'), 0))
    
    # 12. TechSupport (encoded)
    features.append(label_mappings['TechSupport'].get(data.get('TechSupport', 'No'), 0))
    
    # 13. StreamingTV (encoded)
    features.append(label_mappings['StreamingTV'].get(data.get('StreamingTV', 'No'), 0))
    
    # 14. StreamingMovies (encoded)
    features.append(label_mappings['StreamingMovies'].get(data.get('StreamingMovies', 'No'), 0))
    
    # 15. Contract (encoded)
    features.append(label_mappings['Contract'].get(data.get('Contract', 'Month-to-month'), 0))
    
    # 16. PaperlessBilling (encoded)
    features.append(label_mappings['PaperlessBilling'].get(data.get('PaperlessBilling', 'No'), 0))
    
    # 17. PaymentMethod (encoded)
    features.append(label_mappings['PaymentMethod'].get(data.get('PaymentMethod', 'Electronic check'), 2))
    
    # 18. MonthlyCharges (numeric)
    features.append(float(data.get('MonthlyCharges', 0)))
    
    # 19. TotalCharges (numeric)
    features.append(float(data.get('TotalCharges', 0)))
    
    return np.array([features])



@app.route('/')
def home():
    """Render the home page with the prediction form"""
    return render_template('index.html', feature_options=FEATURE_OPTIONS)


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    if model is None:
        return jsonify({'error': 'Model not loaded. Please check the model file.'}), 500
    
    try:
        # Get form data
        data = {
            'gender': request.form.get('gender'),
            'SeniorCitizen': int(request.form.get('SeniorCitizen', 0)),
            'Partner': request.form.get('Partner'),
            'Dependents': request.form.get('Dependents'),
            'tenure': int(request.form.get('tenure', 0)),
            'PhoneService': request.form.get('PhoneService'),
            'MultipleLines': request.form.get('MultipleLines'),
            'InternetService': request.form.get('InternetService'),
            'OnlineSecurity': request.form.get('OnlineSecurity'),
            'OnlineBackup': request.form.get('OnlineBackup'),
            'DeviceProtection': request.form.get('DeviceProtection'),
            'TechSupport': request.form.get('TechSupport'),
            'StreamingTV': request.form.get('StreamingTV'),
            'StreamingMovies': request.form.get('StreamingMovies'),
            'Contract': request.form.get('Contract'),
            'PaperlessBilling': request.form.get('PaperlessBilling'),
            'PaymentMethod': request.form.get('PaymentMethod'),
            'MonthlyCharges': float(request.form.get('MonthlyCharges', 0)),
            'TotalCharges': float(request.form.get('TotalCharges', 0))
        }
        
        # Preprocess input
        features = preprocess_input(data)
        
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        churn_probability = float(prediction_proba[1]) * 100
        no_churn_probability = float(prediction_proba[0]) * 100
        
        result = {
            'prediction': 'Yes' if prediction == 1 else 'No',
            'churn_probability': round(churn_probability, 2),
            'no_churn_probability': round(no_churn_probability, 2),
            'risk_level': 'High' if churn_probability > 70 else 'Medium' if churn_probability > 40 else 'Low'
        }

        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for JSON predictions"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        features = preprocess_input(data)
        
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        return jsonify({
            'churn': bool(prediction),
            'churn_probability': float(prediction_proba[1]),
            'no_churn_probability': float(prediction_proba[0])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
