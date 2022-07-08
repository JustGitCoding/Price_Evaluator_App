# dependencies
import pandas as pd
import joblib

# Function to make predictions based on User input
def evaluate_price(product_id, price, condition, merchant):
    # read in user input from website
    user_input = pd.DataFrame({'id': product_id,
                            'prices_amountmin': price,
                            'prices_condition': condition,
                            'prices_merchant': merchant
                            }, index=[0])

    # Load encoders, scaler, and machine learning model:
    id_encoder = joblib.load('Machine_Learning/ID_Encoder.sav')
    cond_encoder = joblib.load('Machine_Learning/Condition_Encoder.sav')
    merch_encoder = joblib.load('Machine_Learning/Merchant_Encoder.sav')
    X_scaler = joblib.load('Machine_Learning/Data_Scaler.sav')
    ml_model = joblib.load('Machine_Learning/ML_Model.sav')

    # encode user input with id_encoder and merch_encoder
    user_input_encoded = user_input.copy()
    user_input_encoded['id'] = id_encoder.transform(user_input['id'])
    user_input_encoded['prices_condition'] = cond_encoder.transform(user_input['prices_condition'])
    user_input_encoded['prices_merchant'] = merch_encoder.transform(user_input['prices_merchant'])

    # Use X_scaler to transform encoded user input
    user_input_encoded_scaled = X_scaler.transform(user_input_encoded)

    # Return ml model prediction (True indicates price is likely discounted / False indicates price is likely not discounted)
    return ml_model.predict(user_input_encoded_scaled)[0]